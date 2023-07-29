# Import libraries
import pygame
import pygame.midi
from gpiozero import Button
import time

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up output port and instrument sound - ports 2 or 3
audioOutput = pygame.midi.Output(2)
audioOutput.set_instrument(0)

# Set up variabels for GPIO pins
buttonA = Button(15)
buttonB = Button(14)
buttonC = Button(27)
buttonD = Button(17)
buttonE = Button(24)
buttonF = Button(23)

# Set note pitches and volume
c5 = 72
d5 = 74
e5 = 76
f5 = 77
g5 = 79
a5 = 81
velocity = 127

# Declare vars
running = True

# Main loop to run program
while running:
    
    # Let user know program is running
    print("Program Running")

    # If statemnt to play notes when a beam is broken
    if buttonA.is_pressed:
        audioOutput.note_on(c5, velocity)
        time.sleep(2)
        audioOutput.note_off(c5, velocity)
    elif buttonB.is_pressed:
        audioOutput.note_on(d5, velocity)
        time.sleep(2)
        audioOutput.note_off(d5, velocity)
    elif buttonC.is_pressed:
        audioOutput.note_on(e5, velocity)
        time.sleep(2)
        audioOutput.note_off(e5, velocity)
    elif buttonD.is_pressed:
        audioOutput.note_on(f5, velocity)
        time.sleep(2)
        audioOutput.note_off(f5, velocity)
    elif buttonE.is_pressed:
        audioOutput.note_on(g5, velocity)
        time.sleep(2)
        audioOutput.note_off(g5, velocity)
    elif buttonF.is_pressed:
        audioOutput.note_on(a5, velocity)
        time.sleep(2)
        audioOutput.note_off(a5, velocity)
	
# Clean up
audioOutput.close()
pygame.midi.quit()
pygame.quit()

	        


