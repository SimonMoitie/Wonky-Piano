# Import Libraries
import pygame
import pygame.midi
import time
from gpiozero import Button

# Set up variables for GPIO pins
buttonA = Button(15)
buttonB = Button(14)
buttonC = Button(27)
buttonD = Button(17)
buttonE = Button(24)
buttonF = Button(23)

# Set up variables for Midi notes
c4 = 60
d4 = 62
e4 = 64
f4 = 65
g4 = 67
a4 = 69

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Declare variables
port = 2
instrument = 0
velocity = 127
beamBroken = False
running = True
buttonsPlayed = {}
noteDelay = 0.20

# Set up output port and instrument sound
audioOutput = pygame.midi.Output(port)
audioOutput.set_instrument(instrument)

# Dictionary to hold the buttons and map each one with a note
buttons = {
    c4 : buttonA, 
    d4 : buttonB, 
    e4 : buttonC, 
    f4 : buttonD, 
    g4 : buttonE, 
    a4 : buttonF
    }
 
# Function to play notes when beams are broken
def beamNotes():
    
    global beamBroken
           
    # For loop to add each broken beam to new list and start note play
    for note, beam in buttons.items():
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            audioOutput.note_on(note, velocity)
            print(f"{note} is playing")
        # Capture time beams were broken
        startTime = time.time()
            
    # Output message if no beams broken
    if beamBroken == False:
        print("All beams are connected")
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    elif beamBroken == True:
        for beam in buttonsPlayed.values():
            while beam.is_pressed:
                pass
        # Capture time beams no longer broken
        endTime = time.time()
        
        # Stop the notes from playing
        for note in buttonsPlayed.keys():        
            audioOutput.note_off(note, velocity)
            print(f"{note} has stopped")
            
        # Calculate length of time note was played and print to screen
        noteDuration = endTime - startTime
        print(f"Note held for {noteDuration} seconds")	
     	   
    # Reset for next loop through        
    beamBroken = False
    buttonsPlayed.clear()           
            
# Main loop - To keep program running
while running:
    
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
    
    # Recall function to play notes when beams are broken
    beamNotes()
