# Software

**Requirements**: The code runs on a Windows device with [PuTTy](https://www.putty.org/) installed and configured. 
The code also relies on the packages keyboard and pygame.

## Notes
`<username>` and `<password>` on line 45 of [player_launcher.py](player_launcher.py) and line 26 of
[update_firmware.py](update_firmware.py) must be replaced with the username and password of the Raspberry Pi.

The default IP addresses of the minicars are `192.168.2.2<id>`, where `<id>` is the car ID(00-99). To change this, 
modify line 50 in [player_launcher.py](player_launcher.py) and line 26 in [update_firmware.py](update_firmware.py).

The inputs have to be rebound for the joystick in [binds.py](player/binds.py).

## Usage
Enter `python player_launcher.py -n <cars> -c <controller>` into the console. Replace `<cars>` with the numbers of 
the cars to be controlled and `<controller>` with the controller to be used. The current available controllers are 
`Keyboard` and `Joystick` (defaulted to `Keyboard`).

#### Examples

Control minicar 3 with the joystick:

`python player_launcher.py -n 3 -c Joystick`

Control minicars 0, 1, 2, 7 and 10 with the keyboard:

`python player_launcher.py -n 0 1 2 7 10`