# Making a minicar

## Overview
The Raspberry Pi Zero W is configured to connect to a network, have a static IP and have SSH enabled.

The drive motor is controlled through an H-bridge with a PWM pin and two directional pins. It is powered by the 
batteries through a boost converter.

The servo replaces the existing steering motor. It connects to the existing steering with a laser-cut gear tied to a 
servo arm. It is powered by the batteries and controlled with a PWM pin.

The headlights are powered and controlled with a PWM pin.

The three AA batteries are housed in the battery pack and manually enabled by a switch.

The portable charger is placed above the electronics and connected to the Pi with a USB to micro USB cable through a 
manual switch.

The casing is modified to house the components and provide access to the logic switch and enable recharging of the 
portable charger.

**NOTE**: USERNAME, PASSWORD and ID are to be replaced

## Exploded view of a minicar
![exploded view](exploded_view.jpg)

1. Headlights
2. Portable charger
3. Casing screws
4. Gear
5. Servo
6. Lower casing
7. H-bridge
8. Micro SD card
9. USB switch
10. Circuit board
11. Upper casing
12. JST connectors
13. Micro USB cable
14. Boost converter
15. Raspberry Pi Zero W
16. Motor switch
17. Drive motor

## Components
* [8GB micro SD card](https://www.amazon.co.uk/SanDisk-MicroSDHC-Memory-Label-Change/dp/B001D0ROGO/)
* [Raspberry Pi Zero W](https://thepihut.com/products/raspberry-pi-zero-w)
* [Portable charger](https://www.amazon.co.uk/Anker-PowerCore-Aluminum-Portable-Lipstick-Sized-Black/dp/B005QI1A8C)
* USB to micro USB cable
* [USB switch](https://thepihut.com/products/usb-cable-with-switch)
* [Car](https://www.amazon.co.uk/Sport-Official-Licensed-Controlled-RC/dp/B012AT8UUU)
* [3x Eneloop Pro AA battery](https://www.amazon.co.uk/Panasonic-Eneloop-Rechargeable-4BE-Batteries-Black/dp/B00JWC40JY)
* [Proto Bonnet](https://www.amazon.co.uk/SanDisk-MicroSDHC-Memory-Label-Change/dp/B001D0ROGO/)
* [6x Crimp contact](https://uk.rs-online.com/web/p/pcb-connector-contacts/0467598/)
* [3x Female 2 way JST connector](https://uk.rs-online.com/web/p/pcb-connector-housings/2964934/)
* [40x Header pin](https://uk.rs-online.com/web/p/pcb-headers/2518086/)
* Solder
* [3x Male 2 way JST connector](https://uk.rs-online.com/web/p/pcb-headers/4838461/)
* [Male 3 way JST connector](https://uk.rs-online.com/web/p/pcb-headers/4838477/)
* Wire
* Heat shrink
* [H-bridge (L293D)](https://www.amazon.co.uk/L293D-Stepper-Motor-Driver/dp/B008KYMVVY)
* [Boost converter (XL6009)](https://www.amazon.com/eBoot-Converter-Voltage-Adjustable-Step-up/dp/B06XWSV89D/)
* [Gear](gear.pdf)
* Plastic cross servo arm
* [Micro servo motor](https://hobbyking.com/en_us/turnigytm-tgy-50090m-analog-servo-mg-1-6kg-0-08sec-9g.html)
* Hot glue

## Tools
* Crosshead screwdriver
* Plier cutters
* File
* Wire stripper
* Crimping tool
* Soldering iron
* Heat gun
* Multimeter
* Flathead screwdriver
* Hot glue gun

## Software
* Load the micro SD card into a computer
* Use [Rufus](http://rufus.akeo.ie/) (or an alternative) to write [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) 
onto the micro SD card
* Connect the Pi to a monitor and keyboard, place the micro SD card into the Pi and power it
* Login with username: `pi` and password: `raspberry`
* Replace the root password with `PASSWORD` and logout:
    ```commandline
    sudo passwd root
    logout
    ```
* Login as username: `root` and password: `PASSWORD`
* Change the username and password and logout of root:
    ```commandline
    usermod -l USERNAME pi
    usermod -m -d /home/USERNAME USERNAME
    passwd USERNAME
    logout
    ```
* Login as username: `USERNAME` and password: `PASSWORD`
* Lock the account:
    ```commandline
    sudo passwd -l root
    ```
* Change the hostname in hostname and host lookup to minicar-ID:
    ```commandline
    sudo nano /etc/hostname
    sudo nano /etc/hosts
    ```
* Setup the connection to the network giving the Pi a static ip:
    ```commandline
    sudo nano /etc/network/interfaces
    ```
* Enable SSH (navigate to 5, P2) and shutdown:
    ```commandline
    sudo raspi-config
    sudo shutdown now
    ```
* Run [update_firmware.py](../code/update_firmware.py) on a computer connected to the same network:
    ```commandline
    python update_firmware.py -n ID
    ```

## Mechanical
* Unbox the car and unscrew the battery case screw
* Remove the 6 screw holding the top casing down (2 at the front, 2 in the battery case and 2 at the back)
* Take off the upper casing and remove the headlights connector at the circuit board
* Cut the headlights wire at the white connector and remove the connector
* Cut the circuit board wires at the solder joints on the board
* Unscrew and remove the circuit board
* Cut off the circuit board mounts and half of the central right support
* Unscrew the steering motor casing and remove the steering motor
* Unscrew the gear and remove the spring underneath, then screw the gear back on
* Cut off the section with the number 824 and the connected section facing the front from the steering motor casing so 
that the servo can be slid in from the top
* Screw the steering motor casing back on
* Unscrew the 8 screws holding the windows (remove the side mirrors first before taking out the windows)
* Cut off the middle right window
* Cut off the back window to the width of the supports (small indents at the top  of the back window indicate the width)
* Cut off the front right support on the roof at its base
* Screw the windows back onto the upper casing with the side mirrors
* Cut the casing with the black line under the back window to the same width as the hole above it
* File any sharp surfaces that were cut
* Strip and crimp the ends of the cables that were cut (batteries, drive motor, headlights)

## Electrical
![electrical diagram]()
* Solder the header pins onto the Raspberry Pi Zero W's GPIO pins
* Solder short wires to the male connectors and test that the joint will hold
* Cover the joints with heat shrink and fit them in place with the heat gun
* Solder the circuit board as shown above with the H-bridge above and the wires underneath with longer wires going to 
the boost converter (wiring can be cleaned up by soldering to different parts of rails)
* Solder the female header pins to the Proto Bonnet
* Use the multimeter to verify all the connections
* Connect the male connectors to their respective female connectors
* Tune the boost converter to output 7.0V by turning the dial on the blue box clockwise with the flathead screwdriver
(use the multimeter to check the output voltage)
* Connect the Proto Bonnet to the Pi

## Servo setup
* Laser cut the gear in [gear.pdf](gear.pdf)
* Fix the gear onto the servo arm (stripped solid core wire or a paperclip can be threaded through the holes, having 
the ends wrapped together on one end)
* Power the Pi with the portable charger and run [player_launcher.py](../code/player_launcher.py) to put the servo in
the neutral position:
    ```commandline
    python player_launcher.py -n ID
    ```
* Place the servo arm onto the servo such that it is symmetrical about the length and the teeth point away from the 
head
* Place the servo in the modified steering motor casing, such that the gears mesh well and fix the servo in place 
with hot glue

## Closing
* Place the circuit board flat against the top of the battery case with the boost converter behind the back supports
(connecting cables will need to be tucked in the casing)
* Place the portable charger as far back as possible between the back supports
* Connect the USB switch to the portable charger and place it against the middle right window
* Connect the USB switch to the Pi with the USB to micro USB cable
* Close the two sides and screw the casings in place (through the openings, use a screwdriver to move components 
around until the upper casing closes enough to screw it in place)