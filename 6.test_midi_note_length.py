# Import libraries
import pygame
import pygame.midi
import time
from gpiozero import Button

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up output port and instrument sound - ports 2 or 3
audioOutput = pygame.midi.Output(2)
audioOutput.set_instrument(0)

# Set up variabels for GPIO pin
buttonA = Button(15)

# Set note pitch and volume
c5 = 72
velocity = 127

# Declare vars
running = True

# Main loop to run program
while running:
	
	# Let user know program is running
	print("Program Running")
	
	# If statement to play note if beam is broken
	if buttonA.is_pressed:
		# Play Midi note
		audioOutput.note_on(c5, velocity)
		# Get time the note was played
		startTime = time.time()
		
		# While loop to do nothing when beam is broken and note has been played
		# Key to having the beam break length influence the note length (replaces time.sleep())
		while buttonA.is_pressed:
			pass
		
		# When beam is not broken end note
		audioOutput.note_off(c5, velocity)
		#Get time note ended
		endTime = time.time()
		
		# Calculate length of time note was played
		totalTime = endTime - startTime
		
		running = False		
		print(f"Note held for {totalTime} seconds")
				
# Clean up
audioOutput.close()
pygame.midi.quit()
pygame.quit()
