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
buttonA = Button(27)
buttonB = Button(17)
buttonC = Button(15)
buttonD = Button(14)
buttonE = Button(23)
buttonF = Button(24)

# Set up variables for MIDI melody notes and beams
g3 = 55
c4 = 60
d4 = 62
fS4 = 66
g4 = 67
a4 = 69
b4 = 71
c5 = 72
d5 = 74

# Set up variables for sound effects
soundFx1 = 82
soundFx2 = 49
soundFx3 = 45
soundFx4 = 50

# Set up note length variables
wholeNote = 4 # Semi-breve
halfNote = 2 # Minim
quarterNote = 1 # Crotchet
dottedEightNote = 0.75
eighthNote = 0.5 # Quaver
sixteenthNote = 0.25 # Semi-Quaver
thirtySecondNote = 0.125 # Demi-Semi-Quaver

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
instrumentMelody = 80 # MIDI instrument number for the melody
instrumentBeams = 80 # MIDI instrument number for the beams
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
firstAttempt = True
buttonsPlayed = {}
userSolution = []
noteDelay = 0.2
fixedNoteDelay = 0.1
matchingNotes = 0
compareIndex = 0
tempo = 100 # bpm (beats per minute)

# Calculate the length of a whole note (seconds in a minute/tempo)
noteDuration = 60/tempo

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
    (g4, buttonsAndPixels[1][0], *buttonsAndPixels[1][1]),
    (a4, buttonsAndPixels[2][0], *buttonsAndPixels[2][1]), 
    (b4, buttonsAndPixels[3][0], *buttonsAndPixels[3][1]), 
    (c5, buttonsAndPixels[4][0], *buttonsAndPixels[4][1])
    ]
   
buttonsLevelTwo = [
	(g3, buttonsAndPixels[0][0], *buttonsAndPixels[0][1]),
    (d4, buttonsAndPixels[1][0], *buttonsAndPixels[1][1]), 
    (fS4, buttonsAndPixels[2][0], *buttonsAndPixels[2][1]), 
    (g4, buttonsAndPixels[3][0], *buttonsAndPixels[3][1]), 
    (a4, buttonsAndPixels[4][0], *buttonsAndPixels[4][1]),
    (b4, buttonsAndPixels[5][0], *buttonsAndPixels[5][1])  
    ]
    
buttonsLevelThree = [
    (g3, buttonsAndPixels[0][0], *buttonsAndPixels[0][1]),
	(d4, buttonsAndPixels[1][0], *buttonsAndPixels[1][1]),
    (fS4, buttonsAndPixels[2][0], *buttonsAndPixels[2][1]), 
    (g4, buttonsAndPixels[3][0], *buttonsAndPixels[3][1]), 
    (a4, buttonsAndPixels[4][0], *buttonsAndPixels[4][1]),
    (d5, buttonsAndPixels[5][0], *buttonsAndPixels[5][1])
    ]
    
buttonsFixed = [
    (g3, buttonA, *pixelsA),
	(d4, buttonB, *pixelsB),
    (fS4, buttonC, *pixelsC), 
    (g4, buttonD, *pixelsD), 
    (a4, buttonE, *pixelsE), 
    (b4, buttonF, *pixelsF)
    ]
    
# Lists to hold the solution for each level
solutionLevelOne = [b4, a4, g4, c5, b4, a4, g4]
solutionLevelTwo = [g3, b4, d4, g3, a4, fS4, fS4, g4, fS4]
solutionLevelThree = [g3, d5, d4, g3, a4, fS4, fS4, g4, fS4, d4, d5, g4, fS4, d4, d5, d5, g4, fS4, d5]

# Lists to hold the melody notes for each level and map each one with a duration in seconds
# (Using list as melody contains duplicate notes)
levelOneMelody = [
    (b4, eighthNote, *buttonsAndPixels[3][1]), 
    (a4, eighthNote, *buttonsAndPixels[2][1]), 
    (g4, wholeNote, *buttonsAndPixels[1][1]),
    (c5, halfNote, *buttonsAndPixels[4][1]), 
    (b4, eighthNote, *buttonsAndPixels[3][1]),
    (a4, eighthNote, *buttonsAndPixels[2][1]),
    (g4, wholeNote, *buttonsAndPixels[1][1])
    ]
    
levelTwoMelody = [
    (g3, eighthNote, *buttonsAndPixels[0][1]), 
    (b4, eighthNote, *buttonsAndPixels[5][1]), 
    (d4, eighthNote, *buttonsAndPixels[1][1]), 
    (g3, eighthNote, *buttonsAndPixels[0][1]),
    (a4, dottedEightNote, *buttonsAndPixels[4][1]), 
    (fS4, dottedEightNote, *buttonsAndPixels[2][1]),
    (fS4, thirtySecondNote, *buttonsAndPixels[2][1]),
    (g4, sixteenthNote, *buttonsAndPixels[3][1]), 
    (fS4, eighthNote, *buttonsAndPixels[2][1]),
    ]
    
levelThreeMelody = [
    (g3, eighthNote, *buttonsAndPixels[0][1]), 
    (d5, eighthNote, *buttonsAndPixels[5][1]), 
    (d4, eighthNote, *buttonsAndPixels[1][1]), 
    (g3, eighthNote, *buttonsAndPixels[0][1]),
    (a4, dottedEightNote, *buttonsAndPixels[4][1]), 
    (fS4, dottedEightNote, *buttonsAndPixels[2][1]),
    (fS4, thirtySecondNote, *buttonsAndPixels[2][1]), 
    (g4, sixteenthNote, *buttonsAndPixels[3][1]), 
    (fS4, sixteenthNote, *buttonsAndPixels[2][1]),
    (d4, eighthNote, *buttonsAndPixels[1][1]), 
    (d5, eighthNote, *buttonsAndPixels[5][1]), 
    (g4, sixteenthNote, *buttonsAndPixels[3][1]), 
    (fS4, eighthNote, *buttonsAndPixels[2][1]),
    (d4, sixteenthNote, *buttonsAndPixels[1][1]), 
    (d5, dottedEightNote, *buttonsAndPixels[5][1]),
    (d5, sixteenthNote, *buttonsAndPixels[5][1]),
    (g4, sixteenthNote, *buttonsAndPixels[3][1]),
    (fS4, eighthNote, *buttonsAndPixels[2][1]), 
    (d5, eighthNote, *buttonsAndPixels[5][1])
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
            if compareIndex <= 6:
                if userSolution[compareIndex] == solutionLevelOne[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
                    
            elif compareIndex > 6:
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
	
    global matchingNotes, running, compareIndex, completed, firstAttempt
    
    # Play melody on first run through
    if firstAttempt == True:
        playMelodyLevelOne()
        firstAttempt = False
     
    # Recall function to play notes when beams are broken
    levelOneBeamNotes()
    
    # When 7 notes have been played, stop and check if notes are correct
    if len(userSolution) == 7:
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
        if matchingNotes == 7:
            correctSoundFx()
            print(f"Player got all {matchingNotes} notes correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            completed = True
            
        elif matchingNotes <= 6:
            wrongSoundFx()
            print(f"Player got {matchingNotes} out of the 7 notes correct.")    
            time.sleep(1)
            print("Try again...")
            playMelodyLevelOne()
            attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
    
    # When more than 7 notes have been played, solution is incorrect       
    elif len(userSolution) > 7:
        pixels.fill(noColour)
        print("Checking solution...")
        time.sleep(1)
        
         # For loop to check if lists match
        for index in range(len(solutionLevelOne)):
            if solutionLevelOne[index] == userSolution[index]:
                matchingNotes += 1
        
        # Output how well they did
        wrongSoundFx()
        if matchingNotes < 7:
            print(f"Player got {matchingNotes} out of the 7 notes correct.")
        elif matchingNotes == 7:
            print(f"Player got {matchingNotes} out of the 7 notes correct, but has pressed an extra beam by mistake.")    
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
            if compareIndex <= 8:
                if userSolution[compareIndex] == solutionLevelTwo[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
                    
            elif compareIndex > 8:
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
	
    global matchingNotes, running, compareIndex, completed, firstAttempt
    
    # Play melody on first run through
    if firstAttempt == True:
        playMelodyLevelTwo()
        firstAttempt = False
         
    # Recall function to play notes when beams are broken
    levelTwoBeamNotes()
    
    # When 9 notes have been played, stop and check if notes are correct
    if len(userSolution) == 9:
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
        if matchingNotes == 9:
            correctSoundFx()
            print(f"Player got all {matchingNotes} notes correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            completed = True
            
        elif matchingNotes <= 8:
            wrongSoundFx()
            print(f"Player got {matchingNotes} out of the 9 notes correct.")    
            time.sleep(1)
            print("Try again...")
            playMelodyLevelTwo()
            attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
    
    # When more than 9 notes have been played, solution is incorrect       
    elif len(userSolution) > 9:
        pixels.fill(noColour)
        print("Checking solution...")
        time.sleep(1)
        
         # For loop to check if lists match
        for index in range(len(solutionLevelTwo)):
            if solutionLevelTwo[index] == userSolution[index]:
                matchingNotes += 1	
        
        # Output how well they did
        wrongSoundFx()
        if matchingNotes < 9:
            print(f"Player got {matchingNotes} out of the 9 notes correct.")
        elif matchingNotes == 9:
            print(f"Player got {matchingNotes} out of the 9 notes correct, but has pressed an extra beam by mistake.")   
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
            if compareIndex <= 18:
                if userSolution[compareIndex] == solutionLevelThree[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
                    
            elif compareIndex > 18:
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
	
    global matchingNotes, running, compareIndex, completed, firstAttempt
    
    # Play melody on first run through
    if firstAttempt == True:
        playMelodyLevelThree()
        firstAttempt = False
	
    # Recall function to play notes when beams are broken
    levelThreeBeamNotes()
    
    # When than 19 notes have been played, stop and check if notes are correct
    if len(userSolution) == 19:
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
        if matchingNotes == 19:
            correctSoundFx()
            print(f"Player got all {matchingNotes} notes correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            completed = True
            
        elif matchingNotes <= 18:
            wrongSoundFx()
            print(f"Player got {matchingNotes} out of the 19 notes correct.")    
            time.sleep(1)
            print("Try again...")
            playMelodyLevelThree()
            attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
    
    # When more than 19 notes have been played, solution is incorrect        
    elif len(userSolution) > 19:
        pixels.fill(noColour)
        print("Checking solution...")
        time.sleep(1)
        
         # For loop to check if lists match
        for index in range(len(solutionLevelThree)):
            if solutionLevelThree[index] == userSolution[index]:
                matchingNotes += 1	
        
        # Output how well they did
        wrongSoundFx()
        if matchingNotes < 19:
            print(f"Player got {matchingNotes} out of the 19 notes correct.")
        elif matchingNotes == 19:
            print(f"Player got {matchingNotes} out of the 19 notes correct, but has pressed an extra beam by mistake.")   
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

# Main loop - To keep program running
while running:
    
    # Recall function to play one of the three puzzle levels
    while completed == False:
	    levelOnePuzzle()
	    #levelTwoPuzzle() 
	    #levelThreePuzzle()

    # Recall function to play the fixed piano when puzzle completed
    fixedPiano()
            
# Clean up
audioOutput.close()
pygame.midi.quit()
pygame.quit()
