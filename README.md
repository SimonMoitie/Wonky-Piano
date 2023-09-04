# CSC7057 - The Wonky Piano
This is a guide on how to set up the Wonky Piano escape room puzzle using a Raspberry Pi.  
For this guide, you will need a Raspberry Pi running the latest Raspberry Pi OS 6.1 operating system.  

The Wonky Piano source code contains four folders:  
- Development Code - The early code used to design and test different functions of the Wonky Piano.  
- Prototypes - The early developement stages of the working puzzle, also used for first end user testing.  
- Potential Final Fuzzles - The last development stage of the working puzzle, used for final end user testing.  
- client - The main code for the working Wonky Piano escape room puzzle.  


## Installation
To set up the Wonky Piano, the files can be downloaded from the ```client``` folder of the Wonky Piano's source code on GitHub: [https://github.com/SimonMoitie/Wonky-Piano].  
To follow this guide, make sure the ```client``` folder is placed within a folder called ```Code``` in the following directory:
```bash
/home/pi/Code/client
```
It is important to make sure the necessary requirements are installed before running the Wonky Piano.

### Timidity++
To get MIDI sound from the Wonky Piano, Timidity++ will need to be installed.  
To install Timidity++ type into the terminal window:
```bash
sudo apt install timidity
```

### Adafruit CircuitPython Neopixel
For the Wonky Piano to use a WS2812 NeoPixel LED strip, it will need to have the Adafruit CircuitPython Neopixel library installed.  
To install Adafruit CircuitPython Neopixel, type into the terminal window:
``` bash
sudo pip3 install rpi_ws281x adafruit-circuitpyhton-neopixel
```
and make sure Adafruit Blinka is installed:
```bash
sudo python3 -m pip install --force-reinstall adafruit-blinka
```
To use NeoPixles with audio, only GPIO pin 10 is compatible as it uses SPI.  
SPI needs to be enabled on the Rasperry Pi before it is used.  
To open the configuration settings type into the terminal window:
``` bash
sudo raspi-config
```
Next, select option `3 Interace Options`, followed by `I4 SPI` and finally select `Enable SPI`.

### Festival
The Wonky Piano also has text-to-speech capabilities if required.  
To utilise text-to-speech, the Festival library will need to be installed.  
To install festival type into the terminal window:
```bash
sudo apt-get install -y libasound2-plugins festival
```

The Wonky Piano should now have all of the necessary requirements to run on the Raspberry Pi.

## Connecting To The Escape Hub

To run the Wonky Piano from the Escape Hub server using Docker, the necessary requirements need to be installed first.  
To install the requirements, type into the terminal window:
```bash
sudo pip install -r /home/pi/Code/client/requirements.txt
```
This should now enable the Wonky Piano to be visible on the Escape Hub when the sm-client-rt.py is run.  
In the sm-client-rt.py file, the address used to connect to the Escape Hub is set on line 24: 
```python
huburi = "ws://192.168.0.2:8000/connect" # URI of the EscapeHub WS service
```
The 192.168.0.2 can be changed to the IP address of any machine hosting the Docker Escape Hub container.

## Running At Boot
The Wonky Piano software will need to be run at boot to ensure it starts automatically when the Raspberry Pi is turned on.

### rc.local
Before starting the sm-client-rt.py file, Timidity++ needs to be running in the background already.  
To access the rc.local file type into the terminal window:
```bash
sudo nano /etc/rc.local
```
At the end of the script, just above the line exit 0, type:
```python
timidity -iA B16,8 -Os &
```
The following is a breakdown of the command:
- -iA - Specifies the use of the ALSA interface.  
- B16,8 - Sets the buffer size, where 16 is the number of fragments, and 8 is bit size.  
- -Os - Specifies MIDI audio output to the ALSA interface.  
- & - Runs Timidity in the background.

### bashrc
To run the Wonky Piano after Timidity++ has started, access the bashrc file by typing into the terminal window:
```bash
sudo nano /home/pi/.bashrc
```
Go to the last line of the script and type:
```python
echo Running the Wonky Piano at boot
sudo python3 /home/pi/Code/client/sm-client-rt.py
```
This will now start the Wonky Piano software automatically after the boot up process has finished and Timidity++ is running.

## Code Overview
The Wonky Piano operates using two files:
- room_puzzle_theme.py - Contains the variables and functions that form the basis of the Wonky Piano puzzle. 
- sm-client-rt.py - Connects the Wonky Piano puzzle to the Escape Hub server and provides the main code to run the puzzle levels.  
### room_theme_puzzle.py
#### Setting Up The Infrared Beams
The infrared beams are assigned to the LED pixel numbers using a list containing tuples before they are randomised:
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
This ensures that the LED pixel numbers always match with the correct beam after the list order has been randomised.  

To assign notes to the infrared beams of the Wonky Piano, lists are used containing tuples to store the note name, the beam name and the LED pixel numbers. The index numbers from the ```beamsAndPixels``` list are used to access the beam name and pixel numbers:

```python
beamsLevelOne = [
    (g4, beamsAndPixels[1][0], *beamsAndPixels[1][1]),
    (a4, beamsAndPixels[2][0], *beamsAndPixels[2][1]), 
    (b4, beamsAndPixels[3][0], *beamsAndPixels[3][1]), 
    (c5, beamsAndPixels[4][0], *beamsAndPixels[4][1])
    ]
```
There are four functions that are used to play notes when the infrared beams have been broken: ```fixedPiano()```, ```levelOneBeamNotes```, ```levelTwoBeamNotes()``` and ```levelThreeBeamNotes()```.  

As the user is playing the notes, a for loop is used to light up the appropriate pixels over the infrared beam using: 
```python
for note, beam, pixelOne, pixelTwo, pixelThree in beamsLevelOne:
    pixels[pixelOne] = (white)
    pixels[pixelTwo] = (white)
    pixels[pixelThree] = (white) 
    ...
```
and add the note to a new list with: 
```python
    userSolution.append(note)
```
#### Creating Melodies
The melodies are set up using more lists containing tuples to store the note name, note length and LED pixel numbers.  
Again, the index numbers are used from ```beamsAndPixels``` list to access the LED pixel numbers.
```python
levelOneMelody = [
    (c5, halfNote, *beamsAndPixels[4][1]), 
    (b4, eighthNote, *beamsAndPixels[3][1]),
    (a4, eighthNote, *beamsAndPixels[2][1]),
    (g4, halfNote, *beamsAndPixels[1][1])
    ]
```

The tempo of the melody can be set using the tempo variable:
```python
tempo = 90 # bpm (beats per minute)
```
The melody notes are set up using the MIDI numbers that correspond to the desired notes:

```python
g3 = 55
c4 = 60
d4 = 62
fS4 = 66
g4 = 67
a4 = 69
b4 = 71
c5 = 72
d5 = 74
```

The notes of the melodies will play in the order they are sorted in the lists as a for loop is used to start and stop the MIDI sound:
```python
for note, noteLength, pixelOne, pixelTwo, pixelThree in levelOneMelody:
    ...
    audioOutput.note_on(note, velocity)
    ...
    audioOutput.note_off(note, velocity)
```
There are three functions to play the melody for each puzzle level: ```levelOneMelody()```, ```levelTwoMelody()``` and ```levelThreeMelody()```.

#### Puzzle Levels
There are three functions to organise the puzzle levels and check the attempts: ```levelOnePuzzle()```, ```levelTwoPuzzle``` and ```levelThreePuzzle```.  
The puzzle attempts are checked by comparing the userSolution list with the solutionLevel list and comparing how many of the indexes match and incrementing the variable ```matchingNotes```: 
```python 
if len(userSolution) == len(solutionLevelOne):
    ...
    for index in range(len(solutionLevelOne)):
            if solutionLevelOne[index] == userSolution[index]:
                matchingNotes += 1	
```

### sm-client-rt.py
The ```sm-client-rt.py``` file is based on the ```demo-client.py``` file from the Escape Hub. A summary the ```demo-client.py``` code can be seen here: [https://github.com/purplepixie/escape-hub].  

#### Using Threads To Start The Puzzles
The puzzle levels are run in threads. There is a function that starts the threads: 
```python
def startPuzzleLevel(puzzleLevel):
    ...
    puzzleThread = threading.Thread(target=puzzleLevel)
    puzzleThread.start()
```
and a function that stops the threads:
```python    
def stopPuzzleLevel():
    ...
    stopThread.set()
    ...
    puzzleThread.join() 
    stopThread.clear() 
```
#### Playing the Melody Clues
To play the melody clue at any point, there is a functions for each puzzle level: ```levelOneMelody()```, ```levelTwoMelody()``` and ```levelThreeMelody()```.  
Each function works by calling the ```stopPuzzleLevel()``` function to stop the thread, plays the melody clue and then calls the ```startPuzzleLevel()``` function to start the thread again:
```python
def levelOneMelody():
    stopPuzzleLevel()
    ...
    room_theme_puzzle.playMelodyLevelTwo()
    ...
    startPuzzleLevel(roomThemeLevelTwo)
```
#### Running The Puzzle Levels
The order for each puzzle level is organised using three functions: ```roomThemeLevelOne()```, ```roomThemeLevelTwo()``` and ```roomThemeLevelThree()```.  
They contain a while loop to keep the puzzle active whilst it is being played, and they can be stopped at any time from the Escape Hub interface by setting an event flag: ```stopThread.set()``` to break out of the loop: 
```python 
if stopThread.is_set(): 
    break
```
If the puzzle level has been successfully completed the ```completed``` variable from the ```room_theme_puzzle.py``` file will change to true and end the inner while loop to progress to the ```fixedPiano``` function:
```python
while room_theme_puzzle.completed == False:                 
            room_theme_puzzle.levelOnePuzzle()
...
room_theme_puzzle.fixedPiano()
```