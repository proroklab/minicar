"""
This file is the player control.
It enables the player to control one minicar in one of three modes using a controller.

The **username** and **password** on line 44 must be replaced by the username and password of the Raspberry Pi before
running this code.
"""

import argparse
import socket
import struct
import time
import os
import sys
import keyboard
from threading import Thread

from player import controllers


class Player(object):
    """Defines the player object to be controlled externally by a controller"""

    def __init__(self, number, controller, max_speed=0.7, max_angle=0.3125, max_accel=1., max_angle_acc=0.1):
        # Import variables
        self.car_number = number

        # Calculate IP
        self.ip = '192.168.2.{}'.format(200 + number)

        # Assign controller
        if controller == 'keyboard':
            self.controller = controllers.Keyboard(max_speed, max_angle, max_accel, max_angle_acc)
        elif controller == 'joystick':
            self.controller = controllers.Joystick(max_speed, max_angle, max_accel, max_angle_acc)
        else:
            raise ValueError('Invalid controller')

        # Define vairables
        self.remote_port = 6789

    def boot(self):
        """Launches car.py in the Pi"""
        os.system('putty -ssh **username**@{} -pw **password** -m "launch.txt"'.format(self.ip))

    def ping(self):
        """Tests for response"""
        return os.system('ping -n 1 -w 200 {} | find "Reply"'.format(self.ip))

    def run(self):
        """Initiates the Pi and transfers incoming data to the Pi at 100Hz"""
        Thread(target=self.boot).start()
        print('Listening...')
        clean = False
        while self.controller.running:
            self.controller.listen()

            # Check for break
            if keyboard.is_pressed('esc'):
                self.controller.running = False
                clean = True

            # Send data at 100Hz
            buffer = bytearray(
                struct.pack('fff?', self.controller.speed, self.controller.angle, self.controller.brightness,
                            clean))
            s.sendto(buffer, (self.ip, self.remote_port))
            time.sleep(0.01)


def main(car_list):
    """Starts and runs the listed cars"""
    unresponsive = []
    for car_number in car_list:
        players[car_number] = Player(car_number, args.controller)
        response = players[car_number].ping()
        if response == 0:
            players_thread[car_number] = Thread(target=players[car_number].run)
            players_thread[car_number].start()
        elif response == 1:
            del players[car_number]
            print('Player {} unresponsive'.format(car_number))
            unresponsive.append(car_number)

    if len(unresponsive) == 0:
        print('Startup finished\nSending...')

    else:
        print('Cars {} unresponsive\nPress R to retry for unresponsive or Q to stop'.format([*unresponsive]))
        while not keyboard.is_pressed('q'):
            if keyboard.is_pressed('r'):
                main(unresponsive)
        unresponsive = []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Start and manually control a car")
    parser.add_argument('-n', '--cars', nargs='+', type=int, default=None, help='Manual cars')
    parser.add_argument('-c', '--controller', type=str, default='keyboard', help='Controller type')
    args = parser.parse_args()

    if args.cars is None:
        print('No player selected')
        sys.exit(0)

    # Setup socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    players = {}
    players_thread = {}
    main(args.cars)
