# CSC7057 - The Wonky Piano
This is a guide on how to set up the Wonky Piano escape room puzzle for the Raspberry Pi.  
For this guide, the Raspberry Pi will need to be using the latest Raspberry Pi OS 6.1 operating system.  
The Wonky Piano source code contains four folders:  
- Development Code - The early code used to design and test different functions of the Wonky Piano.  
- Protoypes - Early developement stages of the working puzzle, also used for early end user testing.  
- Potential Final Fuzzles - The last development stage of the working puzzle, used for final end user testing.  
- client - The main code for the working Wonky Piano escape room puzzle.  


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
To use NeoPixles with audio, only GPIO 10 pin is compatable as it uses SPI.  
SPI needs to be enabled on the Rasperry Pi before it is used.  
To open the configuration settings type into the terminal window:
``` bash
sudo raspi-config
```
Next select option `3 Interace Options`, followed by `I4 SPI` and select `Enable SPI`.

### Festival
The Wonky Piano also has text-to-speech capabilities if required.  
To utilise text-to-speech, the Festival library will need to be installed.  
To install festival type into the terminal window:
```bash
sudo apt-get install -y libasound2-plugins festival
```

The Wonky Piano should now have all of the necessary requirements to run on the Raspberry Pi.

## Connecting To The EscapeHub

To run the Wonky Piano from the EscapeHub server using Docker, the necessary requirements need to be installed.  
To install the requirements, type into the terminal window:
```bash
sudo pip install -r /home/pi/Code/client/requirements.txt
```
This should now enable the Wonky Piano to visible on the EscapeHub when the sm-client-rt.py is run.  
In the sm-client-rt.py file, the address used to connect to the EscapeHub is set on line 24: 
```python
huburi = "ws://192.168.0.2:8000/connect" # URI of the EscapeHub WS service
```
The 192.168.0.2 can be changed to the IP address of any machine hosting the Docker EscapeHub container.

## Running At Boot
The Wonky Piano software will need to be run at boot to ensure it starts automatically when the Raspberry Pi is turned on.

### rc.local
Before starting the sm-client-rt.py file, Timidity needs to be running in the background already.  
To access the rc.local file type into the terminal window:
```bash
sudo nano /etc/rc.local
```
At the end of the scrpit, just above the line exit 0, type:
```python
timidity -iA B16,8 -Os &
```
-iA specifies the use of the ALSA interface.  
B16,8 sets the buffer size, where 16 is the number of fragments, and 8 is bit size.  
-Os specifies MIDI audio output to the ALSA interface.  
& runs Timidity in the background.

### bashrc
To run the Wonky Paino after Timidity has started, access the bashrc file by typing into the terminal window:
```bash
sudo nano /home/pi/.bashrc
```
Go to the last line of the script and type:
```python
echo Running the Wonky Piano at boot
sudo python3 /home/pi/Code/client/sm-client-rt.py
```
This will now run the Wonky Piano software after the bootup process has finished.

## Code Maintenance
The Wonky Piano runs using two files:
- room_puzzle_theme.py - Contains the variables and functions that form the basis of the Wonky Piano puzzle. 
- sm-client-rt.py - Connects the Wonky Piano puzzle to the Escape Hub server and provides the main hub to run the puzzle levels.  
### room_theme_puzzle.py
Firstly the beams are assigned to the LED pixel numbers using a list containing tuples before being randomised:
```python
beamsAndPixels = [
    (beamA, pixelsA),
    (beamB, pixelsB),
    (beamC, pixelsC),
    (beamD, pixelsD),
    (beamE, pixelsE),
    (beamF, pixelsF)
    ]
random.shuffle(beamsAndPixels)
```
This ensures the LED pixel numbers always match with correct beam after the beam order has been randomised.  

To assign notes to the beams on the Wonky Piano, lists are used containing tuples to store the note name, the beam name and the LED pixel numbers using the index numbers from the beamsAndPixels list, for example:

```python
beamsLevelOne = [
    (g4, beamsAndPixels[1][0], *beamsAndPixels[1][1]),
    (a4, beamsAndPixels[2][0], *beamsAndPixels[2][1]), 
    (b4, beamsAndPixels[3][0], *beamsAndPixels[3][1]), 
    (c5, beamsAndPixels[4][0], *beamsAndPixels[4][1])
    ]
```
There are four functions that are used to play notes when the beams have been broken: ```fixedPiano()```, ```levelOneBeamNotes```, ```levelTwoBeamNotes()``` and ```levelThreeBeamNotes()```.  
As the user is playing the notes, the appropriate pixels light up over the beam using ```pixels[pixel_number] = (pixel_colour)``` and the note is added to a new list: ```userSolution.append(note_name)```

The melodies are set up using using more lists containing tuples to store the note name, note length and LED pixel numbers, for example:

```python
levelOneMelody = [
    (c5, halfNote, *beamsAndPixels[4][1]), 
    (b4, eighthNote, *beamsAndPixels[3][1]),
    (a4, eighthNote, *beamsAndPixels[2][1]),
    (g4, halfNote, *beamsAndPixels[1][1])
    ]
```
The melodies will play in the order they are sorted in the list.  
There are three functions to play the melody for each puzzle level: ```levelOneMelody()```, ```levelTwoMelody()``` and ```levelThreeMelody()```.

There are three functions to organise the puzzle levels and check the attempts: ```levelOnePuzzle()```, ```levelTwoPuzzle``` and ```levelThreePuzzle```.  
The puzzle attempts are checked by comparing the userSolution list with the solutionLevel list: ```if len(userSolution) == len(solutionLevelOne)```.

### sm-client-rt.py
The ```sm-client-rt.py``` file is based on the ```demo-client.py``` file from the Escape Hub. A summary the ```demo-client.py``` code can be seen here: [https://github.com/purplepixie/escape-hub].  
The puzzle levels are run in threads using two functions that start and stop the threads:
```python
def startPuzzleLevel(puzzleLevel):
    global stopThread, puzzleThread
    puzzleThread = threading.Thread(target=puzzleLevel)
    puzzleThread.start()
    
def stopPuzzleLevel():
    global stopThread, puzzleThread
    device['status'] = "Waiting"
    stopThread.set()
    time.sleep(0.5)
    room_theme_puzzle.stopPuzzle()
    puzzleThread.join() 
    stopThread.clear() 
```
There are three functions to stop the current puzzle level, play the melody clue and restart the puzzle level: ```levelOneMelody()```, ```levelTwoMelody()``` and ```levelThreeMelody()```.  
The puzzle levels are organised using three functions: ```roomThemeLevelOne()```, ```roomThemeLevelTwo()``` and ```roomThemeLevelThree()```.  
They contain a while loop to keep the puzzle active whilst it is being played, and they can be stopped at any time by setting an event flag: ```stopThread.set()``` to break out of the loop: ```if stopThread.is_set(): break```. 