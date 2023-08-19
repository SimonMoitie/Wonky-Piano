# CSC7057 The Wonky Piano
This is a guide on how to set up the Wonky Piano escape room puzzle for the Raspberry Pi.
For this guide, the Raspberry Pi will need to be using the latest Raspberry Pi OS 6.1 operating system. 

## Installation
To set up the Wonky piano, download the client folder.
To follow this guide, place the client folder in a folder called Code as shown here:
```bash
/home/pi/Code/client
```
It is important to make sure the necessary requirements are installed before running the Wonky Piano.

### Timidity
To get MIDI sound from the Wonky Piano, Timidity will need to be installed.
To install Timidity type into the terminal window:
 ```bash
sudo apt install timidity
```

### Adafruit CircuitPython Neopixel
For the Wonky Piano to use the LED strip, it will need to have the Adafruit CircuitPython Neopixel library installed.
To install Adafruit CircuitPython Neopixel type into the terminal window:
``` bash
sudo pip3 install rpi_ws281x adafruit-circuitpyhton-neopixel
```
and
```bash
sudo python3 -m pip install --force-reinstall adafruit-blinka
```

### Festival
The Wonky Piano also has text-to-speech capabilities if required.
To utilise text-to-speech, the Festival library will need to be installed.
To install festival type into the terminal window:
```bash
sudo apt-get install -y libasound2-plugins festival
```

The Wonky Piano should now have all of the necessary requirements to run on the Raspberry Pi.

## Running from the EscapeHub

To run the Wonky Piano from the EscapeHub server using Docker, the necessary requirements need to be installed.
To install the requirements, type into the terminal window:
```bash
sudo pip install -r /home/pi/Code/client/requirements.txt
```
This should now enable the Wonky Piano to visible on the EscapeHub when the sm-client-mm.py is run.

## Running At Boot
The Wonky Piano software will need to be run at boot to ensure it starts automatically when the Raspberry Pi is turned on.

### rc.local
Before starting the sm-client-mm.py file, Timidity needs to be running in the background already.
To access the rc.local file type into the terminal window:
```bash
sudo nano /etc/rc.local
```
At the end of the scrpit, just above the line exit 0, type:
```python
timidity -iA B16,8 -Os &
```
-iA specifies the use of the ASLA interface.
B16,8 sets the buffer size, where 16 is the number of fragments, and 8 is bit size.
-Os optimises the settings to run on hardware with lower resources.

### bashrc
To run the Wonky Paino after Timidity has started, access the bashrc file by typing into the terminal window:
```bash
sudo nano /home/pi/.bashrc
```
Go to the last line of the script and type:
```python
echo Running the Wonky Piano at boot
sudo python3 /home/pi/Code/client/sm-client-mm.py
```
This will now run the Wonky Piano software after the bootup process has finished.