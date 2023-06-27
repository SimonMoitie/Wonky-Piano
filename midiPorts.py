import pygame.midi

pygame.midi.init()

# For loop to display MIDI output devices
for i in range(pygame.midi.get_count()):
	device_info = pygame.midi.get_device_info(i)
	device_name = device_info[i]
	print(f"Device ID: {i}, Name: {device_name}")
	
# To start Timidity use: timidity -iA -B2,8 -Os &
