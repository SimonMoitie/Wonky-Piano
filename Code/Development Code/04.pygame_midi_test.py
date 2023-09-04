# Import libraries
import pygame
import pygame.midi
import time

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up output port and instrument sound - ports 2 or 3
outputDevice = pygame.midi.Output(2)
outputDevice.set_instrument(0)

# Set note pitch and volume
c5 = 72
velocity = 127

# Play note
outputDevice.note_on(c5, velocity)
print("Note playing")

time.sleep(3)

# Turn note off
outputDevice.note_off(c5, velocity)
print("Note stopped")

# Clean up
outputDevice.close()
pygame.midi.quit()
