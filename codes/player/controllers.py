"""
controllers.py

This file provides the keyboard control for the player.

To be completed:
- Avoid multiple inputs
"""

import time
import keyboard
import pygame
import sys

from player import binds


class Keyboard(object):
    """Defines the Keyboard object to transfer keyboard inputs into player instructions"""

    def __init__(self,max_speed,max_angle,max_accel,max_angle_acc):
        # Import variables
        self.max_speed = max_speed
        self.max_angle = max_angle
        self.max_accel = max_accel
        self.max_angle_acc = max_angle_acc

        # Define variables
        self.speed = 0.
        self.angle = 0.
        self.brightness = 0.

        # Define variables
        self.control_type = 0
        self.paused = False
        self.error = False
        self.running = True

        self.binds = binds.KeyboardBinds()

    def stop(self):
        """Stops the car"""
        self.speed = -self.speed
        time.sleep(0.5)
        self.speed = 0

    def merge_left(self):
        """Moves the car to the left lane when possible"""
        pass

    def merge_right(self):
        """Moves the car to the right lane when possible"""
        pass

    def accelerate(self,accel):
        """Increases/decreases the speed up to the max speed"""
        self.speed = min(self.max_speed,max(self.speed + accel,-self.max_speed))

    def turn(self,turn):
        """Increases/decreases the turning angle up to the max angle"""
        self.angle = min(self.max_angle,max(self.angle + turn,-self.max_angle))

    def listen(self):
        """Interprets bound inputs"""
        # Quit
        if keyboard.is_pressed(self.binds.escape):
            self.running = False

        # Stop
        if keyboard.is_pressed(self.binds.stop):
            self.stop()

        # Set control type
        if keyboard.is_pressed(self.binds.manual):
            self.control_type = 0
            print('Manual control')
            time.sleep(0.1)

        elif keyboard.is_pressed(self.binds.semiautomatic):
            self.control_type = 1
            print('Semi-automatic control')
            time.sleep(0.1)

        elif keyboard.is_pressed(self.binds.automatic):
            self.control_type = 2
            print('Automatic control')
            time.sleep(0.1)

        # Manual control
        if self.control_type == 0:
            if keyboard.is_pressed(self.binds.forwards):
                self.accelerate(self.max_speed)

            elif keyboard.is_pressed(self.binds.backwards):
                self.accelerate(-self.max_speed)

            else:
                self.speed = 0.

            if keyboard.is_pressed(self.binds.turn_left):
                self.turn(self.max_angle)

            elif keyboard.is_pressed(self.binds.turn_right):
                self.turn(-self.max_angle)

            else:
                self.angle = 0.

        # Semi-automatic control
        elif self.control_type == 1:
            if keyboard.is_pressed(self.binds.accelerate):
                self.accelerate(self.max_speed)

            elif keyboard.is_pressed(self.binds.decelerate):
                self.accelerate(-self.max_speed)

            if keyboard.is_pressed(self.binds.merge_left):
                self.turn(self.max_angle)

            elif keyboard.is_pressed(self.binds.merge_right):
                self.turn(-self.max_angle)

            else:
                self.angle = 0.
                self.stop()

        # Automatic control
        elif self.control_type == 3:
            pass

        # Brightness control
        if keyboard.is_pressed(self.binds.lights_off):
            self.brightness = 0.

        elif keyboard.is_pressed(self.binds.lights_on):
            self.brightness = 1.

        elif keyboard.is_pressed(self.binds.decrease_brightness):
            self.brightness = round(max(0.,self.brightness - 0.1),2)

        elif keyboard.is_pressed(self.binds.increase_brightness):
            self.brightness = round(min(1.,self.brightness + 0.1),2)


class Joystick(object):
    """Defines the Joystick object to transfer joystick inputs into player instructions"""

    def __init__(self,max_speed,max_angle,max_accel,max_angle_acc):
        # Import variables
        self.max_speed = max_speed
        self.max_angle = max_angle
        self.max_accel = max_accel
        self.max_angle_acc = max_angle_acc

        # Define variables
        self.speed = 0.
        self.angle = 90.
        self.brightness = 0.
        self.clean = False
        self.running = True
        self.binds = binds.JoystickBinds()
        self.joystick = None
        self.control_type = 0

        # Initialise joystick
        pygame.display.init()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        if joystick_count == 0:
            print('No joystick connected')
            sys.exit()

        elif joystick_count == 1:
            self.joystick = pygame.joystick.Joystick(0)

        elif joystick_count > 1:
            print('Number of joysticks: {}'.format(joystick_count))

            # Print options
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                print('ID: {}    Name: {}'.format(i,joystick.get_name()))

            # Select options
            if joystick_count > 1:
                while self.joystick is None:
                    for i in range(joystick_count):
                        if keyboard.is_pressed(str(i)):
                            self.joystick = pygame.joystick.Joystick(i)

        self.joystick.init()
        if self.joystick.get_init():
            """
            print('Name: {}'.format(self.joystick.get_name()))
            print('Axes: {}'.format(self.joystick.get_numaxes()))
            print('Trackballs: {}'.format(self.joystick.get_numballs()))
            print('Buttons: {}'.format(self.joystick.get_numbuttons()))
            print('Hats: {}'.format(self.joystick.get_numhats()))
            """
            pass
        else:
            print('Error initialising joystick')

    def __del__(self):
        try:
            self.joystick.quit()
        except (AttributeError,pygame.error):
            pass

    def check(self,bind):
        """Read data from bound location"""
        input_type = bind[0]
        input_location = bind[1]
        if input_type == 'axis':
            return round(self.joystick.get_axis(input_location),2)
        elif input_type == 'button':
            return self.joystick.get_button(input_location)
        elif input_type == 'hat':
            return self.joystick.get_hat(input_location[0])[input_location[1]]

    def accelerate(self,accel):
        """Increases/decreases the speed up to the max speed"""
        self.speed = min(self.max_speed,max(self.speed + accel,-self.max_speed))

    def turn(self,turn):
        """Increases/decreases the turning angle up to the max angle"""
        self.angle = min(self.max_angle,max(self.angle + turn,-self.max_angle))

    def listen(self):
        """Interprets bound inputs"""
        pygame.event.pump()

        # Quit
        if self.check(self.binds.escape) == 1:
            self.running = False
            self.clean = True

        # Set control type
        if self.check(self.binds.manual) == 1:
            self.control_type = 0
            print('Manual control')
            time.sleep(0.1)

        elif self.check(self.binds.semiautomatic) == 1:
            self.control_type = 1
            print('Semi-automatic control')
            time.sleep(0.1)

        elif self.check(self.binds.automatic) == 1:
            self.control_type = 2
            print('Automatic control')
            time.sleep(0.1)

        # Manual control
        if self.control_type == 0:
            self.speed = self.max_speed * -self.check(self.binds.speed)
            self.angle = self.max_angle * -self.check(self.binds.angle)

        # Semi-automatic control
        elif self.control_type == 1:
            self.accelerate(self.max_speed * self.check(self.binds.accelerate) / 10.)
            self.turn(-self.max_angle * self.check(self.binds.turn) / 10.)

        # Automatic control
        elif self.control_type == 2:
            pass

        # Brightness control
        if self.check(self.binds.brightness) > 0.5:
            self.brightness = self.check(self.binds.brightness)

        elif self.check(self.binds.lights_on) == 1:
            self.brightness = 1.

        elif self.check(self.binds.lights_off) == 1:
            self.brightness = 0.
