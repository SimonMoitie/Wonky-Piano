# Import Libraries
import pygame
import pygame.midi
import time

# Set up variables for button Midi notes
note1 = 82
note2 = 49
note3 = 45

# Declare variables
port = 2
instrument1 = 9
instrument2 = 87
velocity = 127

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up output port
audioOutput = pygame.midi.Output(port)


def correctSoundFx():
	
	audioOutput.set_instrument(instrument1)
	
	audioOutput.note_on(note1, velocity)
	time.sleep(1)
	audioOutput.note_off(note1, velocity)

def wrongSoundFx():
	
	audioOutput.set_instrument(instrument2)
	
	audioOutput.note_on(note2, velocity)
	time.sleep(0.2)
	audioOutput.note_off(note2, velocity)
	time.sleep(0.1)
	audioOutput.note_on(note3, velocity)
	time.sleep(0.5)
	audioOutput.note_off(note3, velocity)
	
correctSoundFx()
time.sleep(1)
wrongSoundFx()	
