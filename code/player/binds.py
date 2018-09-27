"""
binds.py

This file provides the binds for each controller.
"""


class KeyboardBinds(object):
    """Binding information for the keyboard controller"""

    def __init__(self):
        self.escape = 'esc'
        self.pause = 'q'

        self.stop = 'e'

        self.manual = '1'
        self.forwards = 'w'
        self.backwards = 's'
        self.turn_left = 'a'
        self.turn_right = 'd'

        self.semiautomatic = '2'
        self.accelerate = 'w'
        self.decelerate = 's'
        self.merge_left = 'a'
        self.merge_right = 'd'

        self.automatic = '3'

        self.lights_off = '-'
        self.lights_on = '='
        self.decrease_brightness = '['
        self.increase_brightness = ']'


class JoystickBinds(object):
    """Binding information for the joystick controller"""

    def __init__(self):
        self.escape = ('button',6)
        self.pause = ('button',7)

        self.stop = ('button',0)

        self.manual = ('button',2)
        self.speed = ('axis',1)
        self.angle = ('axis',4)

        self.semiautomatic = ('button',3)
        self.accelerate = ('hat',(0,1))
        self.turn = ('hat',(0,0))

        self.automatic = ('button',1)

        self.lights_off = ('button',4)
        self.lights_on = ('button',5)
        self.brightness = ('axis',2)
