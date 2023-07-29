# Import Libraries
import pygame
import pygame.midi
import time
import os
import board
import neopixel
import random
from gpiozero import Button

# Set up variables for GPIO pins
buttonA = Button(23)
buttonB = Button(24)
buttonC = Button(27)
buttonD = Button(17)
buttonE = Button(14)
buttonF = Button(15)

# Set up variables for MIDI melody notes and beams
b5 = 83
e6 = 88
fS6 = 90
g6 = 91
a6 = 93
b6 = 95

# Set up variables for sound effects
soundFx1 = 82
soundFx2 = 49
soundFx3 = 45
soundFx4 = 50

# Set up note length variables
wholeNote = 4 # Semi-breve
halfNote = 2 # Minim
quarterNote = 1 # Crotchet
semiNote = 0.5 # Quaver

# Set up LED colour variables
green = 0, 255, 0
red = 255, 0 ,0
white = 255, 255, 255
cyan = 0, 255, 255
pink = 255, 0, 255
yellow = 255, 255, 0
blue = 0, 0, 255
noColour = 0, 0, 0

# Set up LED pixel variables
pixelsA = 23, 24, 25
pixelsB = 19, 20, 21
pixelsC = 14, 15, 16
pixelsD = 10, 11, 12
pixelsE = 5, 6, 7
pixelsF = 1, 2, 3

# Set up MIDI variables
port = 2 # Midi audio port number
instrumentMelody = 8 # MIDI instrument number for the melody
instrumentBeams = 8 # MIDI instrument number for the beams
instrumentCorrectFx = 9 # MIDI instrument number for correct sound fx 
instrumentWrongFx = 87 # MIDI instrument number for wrong sound fx 
instrumentCrowdFx = 126 # MIDI instrument number for crowd sound fx 
velocity = 127 # Set MIDI volume level (between 0 and 127)

# Set up LED variables
pinNumber = board.D10 # Set LED strip GPIO pin number
ledCount = 28 # Set number of pixels on LED strip
ledBrightness = 0.2 # Set LED strip brightness level (between 0 and 1)
updateLed = True # Set if LED colours update manually or automatically

# Set up variables
beamBroken = False
running = True
completed = False
correctNoteOrder = False
attemptingPuzzle = False
buttonsPlayed = {}
userSolution = []
noteDelay = 0.2
fixedNoteDelay = 0.1
matchingNotes = 0
compareIndex = 0
tempo = 60 # bpm (beats per minute)

# Calculate the length of a whole note (seconds in a minute/tempo)
noteDuration = (60/tempo)*4/3

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up LED strip - GPIO pin number, number of LEDs, LED brightness, automatically update colours
pixels = neopixel.NeoPixel(pinNumber, ledCount, brightness = ledBrightness, auto_write = updateLed)

# Set up output port
audioOutput = pygame.midi.Output(port)

# List to map buttons and LEDs and then randomise order
buttonsAndPixels = [
    (buttonA, pixelsA),
    (buttonB, pixelsB),
    (buttonC, pixelsC),
    (buttonD, pixelsD),
    (buttonE, pixelsE),
    (buttonF, pixelsF)
    ]
random.shuffle(buttonsAndPixels)

# List to hold the buttons for each level and map each one with a note and LED pixels
# (Using list to map multiple values)
buttonsLevelOne = [
    (b5, buttonsAndPixels[0][0], *buttonsAndPixels[0][1]),
    (e6, buttonsAndPixels[1][0], *buttonsAndPixels[1][1]), 
    (fS6, buttonsAndPixels[2][0], *buttonsAndPixels[2][1]), 
    (g6, buttonsAndPixels[3][0], *buttonsAndPixels[3][1])
    ]
   
buttonsLevelTwo = [
	(b5, buttonsAndPixels[0][0], *buttonsAndPixels[0][1]),
    (e6, buttonsAndPixels[1][0], *buttonsAndPixels[1][1]), 
    (fS6, buttonsAndPixels[2][0], *buttonsAndPixels[2][1]), 
    (g6, buttonsAndPixels[3][0], *buttonsAndPixels[3][1]), 
    (a6, buttonsAndPixels[4][0], *buttonsAndPixels[4][1]),
    (b6, buttonsAndPixels[5][0], *buttonsAndPixels[5][1]) 
    ]
    
buttonsLevelThree = [
    (b5, buttonsAndPixels[0][0], *buttonsAndPixels[0][1]),
	(e6, buttonsAndPixels[1][0], *buttonsAndPixels[1][1]),
    (fS6, buttonsAndPixels[2][0], *buttonsAndPixels[2][1]), 
    (g6, buttonsAndPixels[3][0], *buttonsAndPixels[3][1]), 
    (a6, buttonsAndPixels[4][0], *buttonsAndPixels[4][1]), 
    (b6, buttonsAndPixels[5][0], *buttonsAndPixels[5][1])
    ]
    
buttonsFixed = [
    (b5, buttonA, *pixelsA),
	(e6, buttonB, *pixelsB),
    (fS6, buttonC, *pixelsC), 
    (g6, buttonD, *pixelsD), 
    (a6, buttonE, *pixelsE), 
    (b6, buttonF, *pixelsF)
    ]
    
# Lists to hold the solution for each level
solutionLevelOne = [b5, e6, g6, fS6, e6]
solutionLevelTwo = [b5, e6, g6, fS6, e6, b6, a6, fS6, e6, g6, fS6, e6, fS6, b5]
solutionLevelThree = [b5, b5, e6, g6, fS6, b5, e6, b6, e6, a6, e6, fS6, b5, e6, g6, fS6, e6, b6, fS6, a6, b5]

# Lists to hold the melody notes for each level and map each one with a duration in seconds
# (Using list as melody contains duplicate notes)
levelOneMelody = [
    (b5, semiNote, *buttonsAndPixels[0][1]), 
    (e6, quarterNote, *buttonsAndPixels[1][1]), 
    (g6, semiNote, *buttonsAndPixels[3][1]), 
    (fS6, semiNote, *buttonsAndPixels[2][1]), 
    (e6, quarterNote, *buttonsAndPixels[1][1])
    ]
    
levelTwoMelody = [
    (b5, semiNote, *buttonsAndPixels[0][1]), 
    (e6, quarterNote, *buttonsAndPixels[1][1]), 
    (g6, semiNote, *buttonsAndPixels[3][1]), 
    (fS6, semiNote, *buttonsAndPixels[2][1]), 
    (e6, quarterNote, *buttonsAndPixels[1][1]),
    (b6, semiNote, *buttonsAndPixels[5][1]),
    (a6, quarterNote, *buttonsAndPixels[4][1]),
    (fS6, quarterNote, *buttonsAndPixels[2][1]),
    (e6, quarterNote, *buttonsAndPixels[1][1]),
    (g6, semiNote, *buttonsAndPixels[3][1]),
    (fS6, semiNote, *buttonsAndPixels[2][1]),
    (e6, quarterNote, *buttonsAndPixels[1][1]),
    (fS6, semiNote, *buttonsAndPixels[2][1]),
    (b5, quarterNote, *buttonsAndPixels[0][1])
    ]
    
levelThreeMelody = [
    (b5, semiNote, *buttonsAndPixels[0][1]), 
    (b5, e6, quarterNote, *buttonsAndPixels[0][1], *buttonsAndPixels[1][1]), 
    (g6, semiNote, *buttonsAndPixels[3][1]), 
    (fS6, semiNote, *buttonsAndPixels[2][1]), 
    (b5, e6, quarterNote, *buttonsAndPixels[0][1], *buttonsAndPixels[1][1]),
    (b6, semiNote, *buttonsAndPixels[5][1]),
    (e6, a6, quarterNote, *buttonsAndPixels[1][1], *buttonsAndPixels[4][1]),
    (e6, fS6, quarterNote, *buttonsAndPixels[1][1], *buttonsAndPixels[2][1]),
    (b5, e6, quarterNote, *buttonsAndPixels[0][1], *buttonsAndPixels[1][1]),
    (g6, semiNote, *buttonsAndPixels[3][1]),
    (fS6, semiNote, *buttonsAndPixels[2][1]),
    (e6, b6, quarterNote, *buttonsAndPixels[1][1], *buttonsAndPixels[5][1]),
    (fS6, a6, semiNote, *buttonsAndPixels[2][1], *buttonsAndPixels[4][1]),
    (b5, quarterNote, *buttonsAndPixels[0][1])
    ]



# Function to play level one Melody
def playMelodyLevelOne():
	# Set the instrument
    audioOutput.set_instrument(instrumentMelody)
    print("Melody is playing")
    
    # For loop to iterate through list, play melody notes and light up LED beam played   
    for note, noteLength, pixelOne, pixelTwo, pixelThree in levelOneMelody:
        pixels[pixelOne] = (cyan)
        pixels[pixelTwo] = (cyan)
        pixels[pixelThree] = (cyan)
        audioOutput.note_on(note, velocity)
        time.sleep(noteLength*noteDuration)
        pixels[pixelOne] = (noColour)
        pixels[pixelTwo] = (noColour)
        pixels[pixelThree] = (noColour)
        audioOutput.note_off(note, velocity)	

# Function to play level two Melody
def playMelodyLevelTwo():
	# Set the instrument
    audioOutput.set_instrument(instrumentMelody)
    print("Melody is playing")
    
    # For loop to iterate through list, play melody notes and light up LED beam played   
    for note, noteLength, pixelOne, pixelTwo, pixelThree in levelTwoMelody:
        pixels[pixelOne] = (cyan)
        pixels[pixelTwo] = (cyan)
        pixels[pixelThree] = (cyan)
        audioOutput.note_on(note, velocity)
        time.sleep(noteLength*noteDuration)
        pixels[pixelOne] = (noColour)
        pixels[pixelTwo] = (noColour)
        pixels[pixelThree] = (noColour)
        audioOutput.note_off(note, velocity)
	    
# Function to play level three Melody
def playMelodyLevelThree():
	# Set the instrument
    audioOutput.set_instrument(instrumentMelody)
    print("Melody is playing")
    
    # For loop to iterate through list, play melody notes and light up LED beam played    
    for notes in levelThreeMelody:
		
		# If statement to play single note or two notes together		
        if len(notes) == 9:
            note1, note2, noteLength, pixelOne, pixelTwo, pixelThree, pixelFour, pixelFive, pixelSix = notes
            pixels[pixelOne] = (cyan)
            pixels[pixelTwo] = (cyan)
            pixels[pixelThree] = (cyan)
            pixels[pixelFour] = (cyan)
            pixels[pixelFive] = (cyan)
            pixels[pixelSix] = (cyan)
            audioOutput.note_on(note1, velocity)
            audioOutput.note_on(note2, velocity)
            time.sleep(noteLength*noteDuration)
            pixels[pixelOne] = (noColour)
            pixels[pixelTwo] = (noColour)
            pixels[pixelThree] = (noColour)
            pixels[pixelFour] = (noColour)
            pixels[pixelFive] = (noColour)
            pixels[pixelSix] = (noColour)
            audioOutput.note_off(note1, velocity)
            audioOutput.note_off(note2, velocity)
	    
        if len(notes) == 5:
            note1, noteLength, pixelOne, pixelTwo, pixelThree = notes
            pixels[pixelOne] = (cyan)
            pixels[pixelTwo] = (cyan)
            pixels[pixelThree] = (cyan)
            audioOutput.note_on(note1, velocity)
            time.sleep(noteLength*noteDuration)
            pixels[pixelOne] = (noColour)
            pixels[pixelTwo] = (noColour)
            pixels[pixelThree] = (noColour)
            audioOutput.note_off(note1, velocity)

# Function to play the correct sound effect	    
def correctSoundFx():
	# Set the instrument
    audioOutput.set_instrument(instrumentCorrectFx)
	
	# Play the sound effect and light up LEDs
    pixels.fill(green)
    audioOutput.note_on(soundFx1, velocity)
    time.sleep(1)
    pixels.fill(noColour)
    audioOutput.note_off(soundFx1, velocity)
    time.sleep(1)

# Function to play the incorrect sound effect
def wrongSoundFx():
	
	# Set instrument
    audioOutput.set_instrument(instrumentWrongFx)
	
	# Play the sound effect and light up LEDs
    pixels.fill(red)
    audioOutput.note_on(soundFx2, velocity)
    time.sleep(0.2)
    pixels.fill(noColour)
    audioOutput.note_off(soundFx2, velocity)
    time.sleep(0.1)
    pixels.fill(red)
    audioOutput.note_on(soundFx3, velocity)
    time.sleep(0.5)
    pixels.fill(noColour)
    audioOutput.note_off(soundFx3, velocity)

# Function to play the applause sound effect	
def applauseSoundFx():
	
	# Set instrument
    audioOutput.set_instrument(instrumentCrowdFx)	    
	
	# Play the sound effect and light up LEDs
    audioOutput.note_on(soundFx4, velocity)
    pixels.fill(green)
    time.sleep(0.2)
    pixels.fill(blue)
    time.sleep(0.2)
    pixels.fill(pink)
    time.sleep(0.2)
    pixels.fill(yellow)
    time.sleep(0.2)
    pixels.fill(green)
    time.sleep(0.2)
    pixels.fill(blue)
    time.sleep(0.2)
    pixels.fill(pink)
    time.sleep(0.2)
    pixels.fill(yellow)
    time.sleep(0.2)
    pixels.fill(white)
    time.sleep(0.2)
    pixels.fill(green)
    time.sleep(0.2)
    pixels.fill(blue)
    time.sleep(0.2)
    pixels.fill(pink)
    time.sleep(0.2)
    pixels.fill(yellow)
    time.sleep(0.2)
    pixels.fill(green)
    time.sleep(0.2)
    pixels.fill(blue)
    time.sleep(0.2)
    pixels.fill(pink)
    time.sleep(0.2)
    pixels.fill(yellow)
    time.sleep(0.2)
    pixels.fill(noColour)
    audioOutput.note_off(soundFx4, velocity)
    
# Function to play the piano when puzzle completed    
def fixedPiano():
    
    global beamBroken, correctNoteOrder
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    if correctNoteOrder == False:
        print("Notes now in the correct order")
        correctNoteOrder = True
        
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(fixedNoteDelay)
                
    # For loop to turn on LEDs over active beams, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in buttonsFixed:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white) 
        
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            audioOutput.note_on(note, velocity)
            pixels[pixelOne] = (cyan)
            pixels[pixelTwo] = (cyan)
            pixels[pixelThree] = (cyan)
                        
    # If no beams broken do nothing
    if beamBroken == False:
        pass
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    elif beamBroken == True:
        for note, beam in buttonsPlayed.items():
            while beam.is_pressed:
                pass
            # Stop the notes from playing
            audioOutput.note_off(note, velocity)
                	   
    # Reset for next loop through        
    beamBroken = False

# Function to play notes for level one when beams are broken
def levelOneBeamNotes():
    
    global beamBroken, compareIndex, attemptingPuzzle
        
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    if attemptingPuzzle == False:
        print("Attempt the puzzle...")
        attemptingPuzzle = True
    
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
                
    # For loop to turn on LEDs over active beams, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelOne:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white)  
        
        # When beam is pressed play note and add to list to compare solution
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            
            # Turn LEDs red or green depending if note played is correct or incorrect
            if compareIndex <= 4:
                if userSolution[compareIndex] == solutionLevelOne[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
                    
            elif compareIndex > 4:
                pixels[pixelOne] = (red)
                pixels[pixelTwo] = (red)
                pixels[pixelThree] = (red) 
            
            # Increase the index each time button pressed
            compareIndex += 1
            
    # If no beams broken do nothing
    if beamBroken == False:
        pass
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    elif beamBroken == True:
        for note, beam in buttonsPlayed.items():
            while beam.is_pressed:
                pass
            # Stop the notes from playing
            audioOutput.note_off(note, velocity)
                	   
    # Reset for next loop through        
    beamBroken = False
    buttonsPlayed.clear() 

# Function to play the level one puzzle    
def levelOnePuzzle():
	
    global matchingNotes, running, compareIndex, completed, attemptingPuzzle
     
    # Recall function to play notes when beams are broken
    levelOneBeamNotes()
    
    # When 5 notes have been played, stop and check if notes are correct
    if len(userSolution) == 5:
        # For loop to turn off the lights over active beams
        for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelOne:
            pixels[pixelOne] = (noColour)
            pixels[pixelTwo] = (noColour)
            pixels[pixelThree] = (noColour)
        
        print("Checking solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelOne)):
            if solutionLevelOne[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 5:
            correctSoundFx()
            print(f"Player got all {matchingNotes} notes correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            completed = True
            
        elif matchingNotes <= 4:
            wrongSoundFx()
            print(f"Player got {matchingNotes} out of the 5 notes correct.")    
            time.sleep(1)
            print("Try again...")
            playMelodyLevelOne()
            attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
    
    # When more than 5 notes have been played, solution is incorrect       
    elif len(userSolution) > 5:
        pixels.fill(noColour)
        print("Checking solution...")
        time.sleep(1)
        
         # For loop to check if lists match
        for index in range(len(solutionLevelOne)):
            if solutionLevelOne[index] == userSolution[index]:
                matchingNotes += 1
        
        # Output how well they did
        wrongSoundFx()
        if matchingNotes < 5:
            print(f"Player got {matchingNotes} out of the 5 notes correct.")
        elif matchingNotes == 5:
            print(f"Player got {matchingNotes} out of the 5 notes correct, but has pressed an extra beam by mistake.")    
        time.sleep(1)
        print("Try again...")
        playMelodyLevelOne()
        attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0  

# Function to play notes for level two when beams are broken
def levelTwoBeamNotes():
    
    global beamBroken, compareIndex, attemptingPuzzle
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    if attemptingPuzzle == False:
        print("Attempt the puzzle...")
        attemptingPuzzle = True
    
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
                
    # For loop to turn on LEDs over active beams, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelTwo:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white) 
        
        # When beam is pressed play note and add to list to compare solution
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            
            # Turn LEDs red or green depending if note played is correct or incorrect
            if compareIndex <= 13:
                if userSolution[compareIndex] == solutionLevelTwo[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
                    
            elif compareIndex > 13:
                pixels[pixelOne] = (red)
                pixels[pixelTwo] = (red)
                pixels[pixelThree] = (red) 
            
            # Increase the index each time button pressed
            compareIndex += 1
            
    # If no beams broken do nothing
    if beamBroken == False:
        pass
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    elif beamBroken == True:
        for note, beam in buttonsPlayed.items():
            while beam.is_pressed:
                pass
            # Stop the notes from playing
            audioOutput.note_off(note, velocity)
                	   
    # Reset for next loop through        
    beamBroken = False
    buttonsPlayed.clear() 

# Function to play the level two puzzle    
def levelTwoPuzzle():
	
    global matchingNotes, running, compareIndex, completed, attemptingPuzzle
         
    # Recall function to play notes when beams are broken
    levelTwoBeamNotes()
    
    # When 14 notes have been played, stop and check if notes are correct
    if len(userSolution) == 14:
        # For loop to turn off the lights over active beams
        for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelTwo:
            pixels[pixelOne] = (noColour)
            pixels[pixelTwo] = (noColour)
            pixels[pixelThree] = (noColour)
        
        print("Checking solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelTwo)):
            if solutionLevelTwo[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 14:
            correctSoundFx()
            print(f"Player got all {matchingNotes} notes correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            completed = True
            
        elif matchingNotes <= 13:
            wrongSoundFx()
            print(f"Player got {matchingNotes} out of the 14 notes correct.")    
            time.sleep(1)
            print("Try again...")
            playMelodyLevelTwo()
            attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
    
    # When more than 14 notes have been played, solution is incorrect       
    elif len(userSolution) > 14:
        pixels.fill(noColour)
        print("Checking solution...")
        time.sleep(1)
        
         # For loop to check if lists match
        for index in range(len(solutionLevelTwo)):
            if solutionLevelTwo[index] == userSolution[index]:
                matchingNotes += 1	
        
        # Output how well they did
        wrongSoundFx()
        if matchingNotes < 14:
            print(f"Player got {matchingNotes} out of the 14 notes correct.")
        elif matchingNotes == 14:
            print(f"Player got {matchingNotes} out of the 14 notes correct, but has pressed an extra beam by mistake.")   
        time.sleep(1)
        print("Try again...")
        playMelodyLevelTwo()
        attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0  
        
# Function to play notes for level three when beams are broken
def levelThreeBeamNotes():
    
    global beamBroken, compareIndex, attemptingPuzzle
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    if attemptingPuzzle == False:
        print("Attempt the puzzle...")
        attemptingPuzzle = True
    
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)     
           
    # For loop to turn on LEDs over active beams, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelThree:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white) 
        
        # When beam is pressed play note and add to list to compare solution
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            
            # Turn LEDs red or green depending if note played is correct or incorrect
            if compareIndex <= 20:
                if userSolution[compareIndex] == solutionLevelThree[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
                    
            elif compareIndex > 20:
                pixels[pixelOne] = (red)
                pixels[pixelTwo] = (red)
                pixels[pixelThree] = (red) 
            
            # Increase the index each time button pressed
            compareIndex += 1
                        
    # If no beams broken do nothing
    if beamBroken == False:
        pass
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    elif beamBroken == True:
        for note, beam in buttonsPlayed.items():
            while beam.is_pressed:
                pass
            # Stop the notes from playing
            audioOutput.note_off(note, velocity)
                	   
    # Reset for next loop through        
    beamBroken = False
    buttonsPlayed.clear() 

# Function to play the level three puzzle    
def levelThreePuzzle():
	
    global matchingNotes, running, compareIndex, completed, attemptingPuzzle
	
    # Recall function to play notes when beams are broken
    levelThreeBeamNotes()
    
    # When than 21 notes have been played, stop and check if notes are correct
    if len(userSolution) == 21:
        # For loop to turn off the lights over active beams
        for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelThree:
            pixels[pixelOne] = (noColour)
            pixels[pixelTwo] = (noColour)
            pixels[pixelThree] = (noColour)
            
        print("Checking solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelThree)):
            if solutionLevelThree[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 21:
            correctSoundFx()
            print(f"Player got all {matchingNotes} notes correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            completed = True
            
        elif matchingNotes <= 20:
            wrongSoundFx()
            print(f"Player got {matchingNotes} out of the 21 notes correct.")    
            time.sleep(1)
            print("Try again...")
            playMelodyLevelThree()
            attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
    
    # When more than 21 notes have been played, solution is incorrect        
    elif len(userSolution) > 21:
        pixels.fill(noColour)
        print("Checking solution...")
        time.sleep(1)
        
         # For loop to check if lists match
        for index in range(len(solutionLevelThree)):
            if solutionLevelThree[index] == userSolution[index]:
                matchingNotes += 1	
        
        # Output how well they did
        wrongSoundFx()
        if matchingNotes < 21:
            print(f"Player got {matchingNotes} out of the 21 notes correct.")
        elif matchingNotes == 21:
            print(f"Player got {matchingNotes} out of the 21 notes correct, but has pressed an extra beam by mistake.")   
        time.sleep(1)
        print("Try again...")
        playMelodyLevelThree()
        attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0  
        
# Function to print puzzle instructions to screen    
def instructions():
	print("Instructions playing")
	os.system('echo "Can you fix me, by playing the notes, in the correct, order" | festival --tts')
	time.sleep(1)

# Start the puzzle
print("The puzzle is running...")
	
# Recall function to print instructions
instructions()

# Recall function to play one of the three melodies
#playMelodyLevelOne()
playMelodyLevelTwo()
#playMelodyLevelThree()

# Main loop - To keep program running
while running:
    
    # Recall function to play one of the three puzzle levels
    while completed == False:
	    #levelOnePuzzle()
	    levelTwoPuzzle() 
	    #levelThreePuzzle()

    # Recall function to play the fixed piano when puzzle completed
    fixedPiano()
            
# Clean up
audioOutput.close()
pygame.midi.quit()
pygame.quit()
