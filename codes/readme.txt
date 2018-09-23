The player_launcher.py is the main executable script.

Usage: python player_launcher.py [-n] [-c]

Options:
    -n      IDs of the cars to launch. All the cars in the list will be controlled by the keyboard/joystick input simutaneously.
    -c      The controller to use. Currently only "keyboard" and "joystick" are available.

The default IP addresses of the minicars are 192.168.2.2**, where ** is the car ID. 
For example, the IP address of the minicar with ID 5 is 192.168.2.205.
If you want to change the IP setting, please modify line 30 of player_launcher.py correspondingly.

Important: The **username** and **password** in line 45 of player_launcher.py must be replaced by the actual username and password 
of the Raspberry Pi before running the code.