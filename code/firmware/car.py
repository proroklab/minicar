"""
This file provides low-level control for the minicar.
It is to be uploaded to the SD card on the Raspberry Pi 0W.

The library RPi.GPIO is part of Raspbian
"""

import RPi.GPIO as io
import select
import signal
import socket
import struct
import sys
import time


class Output(object):
    """Defines the Output object to send inputs to the components"""

    def __init__(self, pwm_pin, neutral_duty_cycle=0., duty_cycle_range=(0., 99.)):
        # Localise variables
        self.neutral_duty_cycle = neutral_duty_cycle
        self.min_value = duty_cycle_range[0]
        self.max_value = duty_cycle_range[1]

        # Set starting values
        self.duty_cycle = 0.
        self.prev_time = time.time()

        # Setup PWM pins at 100 Hz
        io.setup(pwm_pin, io.OUT)
        self.pwm_pin = io.PWM(pwm_pin, 100)
        self.pwm_pin.start(0)

    def __del__(self):
        self.pwm_pin.stop()

    def set(self, desired_cycle):
        """Assigns a duty cycle to the component within range"""
        # Maintain the duty cycle within the maximum range
        desired_cycle = min(self.max_value, max(desired_cycle, self.min_value))

        # Set duty cycle for pin
        self.pwm_pin.ChangeDutyCycle(desired_cycle)


class Motor(object):
    """Defines Motor object to control GPIO pins and Output object"""

    def __init__(self, pwm_pin, gpio_pins, neutral_duty_cycle=0., duty_cycle_range=(0., 99.)):
        self.motor = Output(pwm_pin, neutral_duty_cycle, duty_cycle_range)
        self.gpio_pins = gpio_pins
        io.setup(self.gpio_pins, io.OUT)

    def set(self, desired_cycle):
        """Assign output duty cycle and motor direction"""
        self.motor.set(abs(desired_cycle))

        if desired_cycle < 0.:
            io.output(self.gpio_pins[0], True)
            io.output(self.gpio_pins[1], False)
        elif desired_cycle >= 0.:
            io.output(self.gpio_pins[0], False)
            io.output(self.gpio_pins[1], True)


def cleanup(signal=None, frame=None):
    """Default cars, clean pins and exit program"""
    print('Cleaning up...')
    motor.set(motor.motor.neutral_duty_cycle)
    servo.set(servo.neutral_duty_cycle)
    led.set(led.neutral_duty_cycle)
    time.sleep(1)
    io.cleanup()
    sys.exit(0)


# Find local IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('192.168.2.1', 1))
local_ip = s.getsockname()[0]

if local_ip is None:
    raise ValueError('Local IP invalid')

# Bind to UDP port
print('Binding to UDP port...')
local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_socket.bind((local_ip, 6789))  # Local port = 6789
local_socket.settimeout(None)
local_socket.setblocking(False)

# Intercept Ctrl+C.
signal.signal(signal.SIGINT, cleanup)

# Initiate GPIO
io.setmode(io.BCM)

# Setup outputs
motor = Motor(4, [17, 25])
servo = Output(6, 15., (12.5, 17.5))
led = Output(16)

# Define control variables
speed = 0.
angle = 0.
brightness = 0.
done = False

print('Listening...')

# Main loop
while not done:
    # Purge all messages
    data = None
    while select.select([local_socket], [], [], 0)[0]:
        data, _ = local_socket.recvfrom(3 * 4 + 1)
    if data is None:
        time.sleep(1. / 100.)  # The car is updated at 100Hz
        continue

    # Receive data as 3 floats and 1 boolean
    speed, angle, brightness, done = struct.unpack('fff?', data)

    # Convert desired values to duty cycles
    speed_cycle = float(speed) * 200. / 3.
    angle_cycle = float(angle) * 12 + 15
    brightness_cycle = float(brightness) * 100.

    # Update desired values
    motor.set(speed_cycle)
    servo.set(angle_cycle)
    led.set(brightness_cycle)

s.close()
cleanup()
