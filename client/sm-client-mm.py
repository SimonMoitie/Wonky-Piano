"""
This file is part of escape-hub.

Escape-hub is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Escape-hub is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with escape-hub. If not, see <https://www.gnu.org/licenses/>.

Escape-hub is Copyright (C) 2023 David Cutting (dcutting@purplepixie.org; http://purplepixie.org/dave; http://davecutting.uk), all rights reserved.
"""

"""
Escape-hub demo client
"""

import time
import threading
import random
import websocket
from hubclient import hubclient
import my_melody_puzzle

huburi = "ws://192.168.0.24:8000/connect" # URI of the EscapeHub WS service
device = { # a dictionary containing our device details
    "room": "1", # ID of the room we are to register to
    "name": "Wonky Piano", # display name of the device
    "status": "Waiting", # textual status for management display
    "actions": [ # list of actions (of empty list!)
        {
            "actionid": "LEVELONE", # the ID we will receive for this action
            "name": "Puzzle Level One", # friendly name for display in the hub
            "enabled": True # is this action currently available
        },
        {
            "actionid": "LEVELONEMELODY", 
            "name": "Level One Melody", 
            "enabled": False
        },
        {
            "actionid": "LEVELTWO", 
            "name": "Puzzle Level Two", 
            "enabled": True
        },
        {
            "actionid": "LEVELTWOMELODY", 
            "name": "Level Two Melody", 
            "enabled": False
        },
        {
            "actionid": "LEVELTHREE", 
            "name": "Puzzle Level Three", 
            "enabled": True
        },
        {
            "actionid": "LEVELTHREEMELODY", 
            "name": "Level Three Melody", 
            "enabled": False
        },
        {
            "actionid": "STOPPUZZLE", 
            "name": "Stop Puzzle", 
            "enabled": False
        }
    ]
}

# Set variables
running = True
stopThread = threading.Event()

# Function to reset the variables when puzzle is stopped
def resetVariables():
    my_melody_puzzle.beamBroken = False
    my_melody_puzzle.completed = False
    my_melody_puzzle.correctNoteOrder = False
    my_melody_puzzle.attemptingPuzzle = False
    my_melody_puzzle.firstAttempt = True
    my_melody_puzzle.buttonsPlayed = {}
    my_melody_puzzle.userSolution = []
    my_melody_puzzle.matchingNotes = 0
    my_melody_puzzle.compareIndex = 0

# Function to run the level one puzzle
def myMelodyLevelOne():
    
    global stopThread
            
    print("Level one is playing...")
    
    # Main loop - To keep program running
    while running:
        
        # Recall function to play one of the three puzzle levels
        while my_melody_puzzle.completed == False:
                            
            my_melody_puzzle.levelOnePuzzle()
            
            # Break out of loop if "stop puzzle" is pressed
            if stopThread.is_set():
                break
        
        if stopThread.is_set():
            break
            
        # Recall function to play the fixed piano when puzzle completed
        my_melody_puzzle.fixedPiano()
    
# Function to run the level two puzzle
def myMelodyLevelTwo():
    
    global stopThread
    
    print("Level two is playing...")
    
    # Main loop - To keep program running
    while running:
        
        # Recall function to play one of the three puzzle levels
        while my_melody_puzzle.completed == False:
                            
            my_melody_puzzle.levelTwoPuzzle()
            
            # Break out of loop if "stop puzzle" is pressed
            if stopThread.is_set():
                break
                
        if stopThread.set_set():
            break
                    
        # Recall function to play the fixed piano when puzzle completed
        my_melody_puzzle.fixedPiano()
            
# Function to run the level three puzzle
def myMelodyLevelThree():
    
    global stopThread
    
    print("Level three is playing...")
    
    # Main loop - To keep program running
    while running:
    
        # Recall function to play one of the three puzzle levels
        while my_melody_puzzle.completed == False:
            
            my_melody_puzzle.levelThreePuzzle()
            
            # Break out of loop if "stop puzzle" is pressed
            if stopThread.is_set():
                break
        
        if stopThread.is_set():
            break
        
        # Recall function to play the fixed piano when puzzle completed
        my_melody_puzzle.fixedPiano()
                
# Functions to start and stop the threads
def startPuzzleLevel(puzzleLevel):
    global stopThread, puzzleThread
    puzzleThread = threading.Thread(target=puzzleLevel)
    puzzleThread.start()
    
def stopPuzzleLevel():
    global stopThread, puzzleThread
    device['status'] = "Waiting"
    stopThread.set()
    time.sleep(0.5)
    my_melody_puzzle.stopPuzzle()
    puzzleThread.join() 
    stopThread.clear()  
    
# Functions to play the melodies   
def levelOneMelody():
    stopPuzzleLevel()
    print("Playing level one melody...")
    my_melody_puzzle.playMelodyLevelOne()
    device['actions'][1]['enabled'] = True
    device['status'] = "Level one running"
    hub.Update(device)
    my_melody_puzzle.userSolution.clear()
    my_melody_puzzle.matchingNotes = 0
    my_melody_puzzle.compareIndex = 0
    startPuzzleLevel(myMelodyLevelOne)

def levelTwoMelody():
    stopPuzzleLevel()
    print("Playing level two melody...")
    my_melody_puzzle.playMelodyLevelTwo()
    device['actions'][3]['enabled'] = True
    device['status'] = "Level two running"
    hub.Update(device)
    my_melody_puzzle.userSolution.clear()
    my_melody_puzzle.matchingNotes = 0
    my_melody_puzzle.compareIndex = 0
    startPuzzleLevel(myMelodyLevelTwo)

def levelThreeMelody():
    stopPuzzleLevel()
    print("Playing level three melody...")
    my_melody_puzzle.playMelodyLevelThree()
    device['actions'][5]['enabled'] = True
    device['status'] = "Level three running"
    hub.Update(device)
    my_melody_puzzle.userSolution.clear()
    my_melody_puzzle.matchingNotes = 0
    my_melody_puzzle.compareIndex = 0
    startPuzzleLevel(myMelodyLevelThree)
    
def ActionHandler(actionid): # handler when we receive an action for us
    global stopThread
    print("Action handler for ID "+actionid)
    # for the demo we will toggle i.e. ACTONE will disable ONE and enable TWO and vice-versa
    if actionid == "LEVELONE":
        device['actions'][0]['enabled'] = False
        device['actions'][1]['enabled'] = True
        device['actions'][2]['enabled'] = False
        device['actions'][4]['enabled'] = False
        device['actions'][6]['enabled'] = True
        device['status'] = "Level one running"
        hub.Update(device)
        # Start puzzle levelone
        startPuzzleLevel(myMelodyLevelOne)
    elif actionid == "LEVELONEMELODY":
        device['actions'][1]['enabled'] = False
        device['status'] = "Level one melody playing"
        hub.Update(device)
        # Play puzzle one melody clue
        levelOneMelody()
    elif actionid == "LEVELTWO":
        device['actions'][0]['enabled'] = False
        device['actions'][2]['enabled'] = False
        device['actions'][3]['enabled'] = True
        device['actions'][4]['enabled'] = False
        device['actions'][6]['enabled'] = True
        device['status'] = "Level two running"
        hub.Update(device)
        # Start puzzle level two
        startPuzzleLevel(myMelodyLevelTwo)
    elif actionid == "LEVELTWOMELODY":
        device['actions'][3]['enabled'] = False
        device['status'] = "Level two melody playing"
        hub.Update(device)
        # Play puzzle two melody clue
        levelTwoMelody()
    elif actionid == "LEVELTHREE":
        device['actions'][0]['enabled'] = False
        device['actions'][2]['enabled'] = False
        device['actions'][4]['enabled'] = False
        device['actions'][5]['enabled'] = True
        device['actions'][6]['enabled'] = True
        device['status'] = "Level three running"
        hub.Update(device)
        # Start puzzle level three
        startPuzzleLevel(myMelodyLevelThree)
    elif actionid == "LEVELTHREEMELODY":
        device['actions'][5]['enabled'] = False
        device['status'] = "Level three melody playing"
        hub.Update(device)
        # Play level three melody clue
        levelThreeMelody()
    elif actionid == "STOPPUZZLE":
        device['actions'][0]['enabled'] = True
        device['actions'][1]['enabled'] = False
        device['actions'][2]['enabled'] = True
        device['actions'][3]['enabled'] = False
        device['actions'][4]['enabled'] = True
        device['actions'][5]['enabled'] = False
        device['actions'][6]['enabled'] = False
        device['status'] = "Stopping puzzle"
        hub.Update(device)
        # Stop puzzle
        stopPuzzleLevel()
        resetVariables() 
    else:
        print("Unknown action") # useful for debug
    # and we update this state i.e. push it back to the hub
    hub.Update(device)

hub = hubclient() # the instance of the hubclient

hub.setDebug(True) # will output LOTS to the console

hub.actionHandler = ActionHandler # assign the function above to handle (receive) actions for us

print("Startup")

print("Connecting to EscapeHub via "+huburi)

hub.Connect(huburi)

print("Registering Device")
myid = hub.Register(device)

# Run program and ensure everything is closed down properly on CTRL + C
try:
    while True: # infinite loop for our device logic
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Closing program...")
    
finally:    
    # Tidy up
    my_melody_puzzle.audioOutput.close()
    my_melody_puzzle.pygame.midi.quit()
    my_melody_puzzle.pygame.quit()
