# Import Libraries
import pygame
import pygame.midi
import time

# Set up variables for Midi notes
c4 = 60
d4 = 62
e4 = 64
f4 = 65
g4 = 67
a4 = 69
b4 = 71
c5 = 72

# Set up note length variables
wholeNote = 1 # Semi-breve
halfNote = 0.5 # Minim
quarterNote = 0.25 # Crotchet
seminote = 0.125 # Quaver

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Declare variables
port = 2
instrument = 0
velocity = 127
running = True
tempo = 60 # bpm (beats per minute)

# Calculate the length of a whole note (seconds in a minute/tempo)
noteDuration = 60/tempo

# Set up output port and instrument sound
audioOutput = pygame.midi.Output(port)
audioOutput.set_instrument(instrument)

# Dictionary to hold the notes and map each one with a duration in seconds
melody = {
    c4 : wholeNote, 
    d4 : halfNote,
    e4 : halfNote,
    f4 : crotchet,
    g4 : crotchet,
    a4 : quaver,
    b4 : quaver,
    c5 : wholeNote
    }

def playMelody():
    # For loop to iterate through dictonary and play a melody    
    for note, noteLength in melody.items():
	    audioOutput.note_on(note, velocity)
	    # Calculate note length from current tempo
	    time.sleep(noteLength*noteDuration)
	    audioOutput.note_off(note, velocity)

# Main loop
while running:
	
	# Recall function to play a melody
	playMelody()
	
	# Stop loop to exit program
	break	
	
# Clean up
audioOutput.close()
pygame.midi.quit()
pygame.quit()
