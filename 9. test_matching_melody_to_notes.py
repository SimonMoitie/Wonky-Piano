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

# Set up variables for button Midi notes
note1 = 61
note2 = 63
note3 = 68 
note4 = 70
note5 = 72

# Declare variables
port = 2
instrument = 0
velocity = 127
beamBroken = False
running = True
buttonsPlayed = {}
userSolution = []
noteDelay = 0.1
matchingNotes = 0

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up output port and instrument sound
audioOutput = pygame.midi.Output(port)
audioOutput.set_instrument(instrument)

# Dictionary to hold the buttons and map each one with a note
buttons = {
    note1 : buttonA, 
    note2 : buttonB, 
    note3 : buttonC, 
    note4 : buttonD, 
    note5 : buttonE
    }

# List to hold the notes and map each one with a duration in seconds
melodyCloseEncounters = [note4, note5, note3, note1, note2]

def playMelody():
    # For loop to iterate through dictonary and play a melody    
    for note in melodyCloseEncounters:
	    audioOutput.note_on(note, velocity)
	    time.sleep(1)
	    audioOutput.note_off(note, velocity)	

# Function to play notes when beams are broken
def beamNotes():
    
    global beamBroken
           
    # For loop to add each broken beam to new list and start note play
    for note, beam in buttons.items():
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            userSolution
            audioOutput.note_on(note, velocity)
            
    # Output message if no beams broken
    if beamBroken == False:
        pass
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
                	   
    # Reset for next loop through        
    beamBroken = False
    buttonsPlayed.clear() 

# Function to print puzzle instructions to screen    
def instructions():
	print("The game has started...")
	time.sleep(1)
	print("Listen to the melody and try to play it back!")
	time.sleep(1)
	
# Recall function to print instructions
instructions()
playMelody()
print("Your turn..")

# Main loop - To keep program running
while running:
    
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
     
    # Recall function to play notes when beams are broken
    beamNotes()
    
    if len(userSolution) == 5:
        print("Lets check your solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(melodyCloseEncounters)):
            if melodyCloseEncounters[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 5:
            print(f"Well done! You got all {matchingNotes} correct!")
            break;
        elif matchingNotes >= 3 and matchingNotes <= 4:
            print(f"Not a bad attempt, you got {matchingNotes} out of the 5 notes correct.")
        elif matchingNotes >= 1 and matchingNotes <= 2:
            print(f"Not great, you got {matchingNotes} out of the 5 notes correct.")
        elif matchingNotes == 0:
            print(f"Did you even try? {matchingNotes} out of 5 notes correct.")
        
        # Empty list to try again
        userSolution.clear()
        print("Try again..")
        matchingNotes = 0
        
# Clean up
audioOutput.close()
pygame.midi.quit()
pygame.quit()
