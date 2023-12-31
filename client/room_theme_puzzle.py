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
beamA = Button(27)
beamB = Button(17)
beamC = Button(15)
beamD = Button(14)
beamE = Button(23)
beamF = Button(24)

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

# Set the tempo for the puzzle melodies
tempo = 90 # bpm (beats per minute)

# Calculate the length of a quarter note
noteDuration = 60/tempo # (seconds in a minute/tempo)

# Set up MIDI variables
instrumentMelody = 1 # MIDI instrument number for the melody
instrumentBeams = 1 # MIDI instrument number for the beams
instrumentCorrectFx = 9 # MIDI instrument number for correct sound fx 
instrumentWrongFx = 87 # MIDI instrument number for wrong sound fx 
instrumentCrowdFx = 126 # MIDI instrument number for crowd sound fx
port = 2 # Midi audio port number 
velocity = 127 # Set MIDI volume level (between 0 and 127)

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
pixelsA = 6, 7, 8
pixelsB = 11, 12, 13
pixelsC = 16, 17, 18
pixelsD = 21, 22, 23
pixelsE = 25, 26, 27
pixelsF = 30, 31, 32

# Set up LED variables
pinNumber = board.D10 # Set LED strip GPIO pin number
ledCount = 39 # Set number of pixels on LED strip
ledBrightness = 0.2 # Set LED strip brightness level (between 0 and 1)
updateLed = True # Set if LED colours update manually or automatically

# Set up LED strip - GPIO pin number, number of LEDs, LED brightness, automatically update colours
pixels = neopixel.NeoPixel(pinNumber, ledCount, brightness = ledBrightness, auto_write = updateLed)

# Set up variables
beamBroken = False
completed = False
correctNoteOrder = False
attemptingPuzzle = False
firstAttempt = True
beamPressed = False
beamsPlayed = {}
userSolution = []
noteDelay = 0.2
fixedNoteDelay = 0.1
ledFlash = 0.2
matchingNotes = 0
compareIndex = 0
startTime = 0
endTime = 0
resetTime = 15

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up output port
audioOutput = pygame.midi.Output(port)

# List containing tuples to map beams and LEDs, and then randomise order
# (Using list to map multiple values)
beamsAndPixels = [
    (beamA, pixelsA),
    (beamB, pixelsB),
    (beamC, pixelsC),
    (beamD, pixelsD),
    (beamE, pixelsE),
    (beamF, pixelsF)
    ]
random.shuffle(beamsAndPixels)

# Lists containing tuples to hold the beams for each level and assign each one with a note and LED pixels
beamsLevelOne = [
    (g4, beamsAndPixels[1][0], *beamsAndPixels[1][1]),
    (a4, beamsAndPixels[2][0], *beamsAndPixels[2][1]), 
    (b4, beamsAndPixels[3][0], *beamsAndPixels[3][1]), 
    (c5, beamsAndPixels[4][0], *beamsAndPixels[4][1])
    ]
   
beamsLevelTwo = [
	(g3, beamsAndPixels[0][0], *beamsAndPixels[0][1]),
    (d4, beamsAndPixels[1][0], *beamsAndPixels[1][1]), 
    (fS4, beamsAndPixels[2][0], *beamsAndPixels[2][1]), 
    (g4, beamsAndPixels[3][0], *beamsAndPixels[3][1]), 
    (a4, beamsAndPixels[4][0], *beamsAndPixels[4][1]),
    (b4, beamsAndPixels[5][0], *beamsAndPixels[5][1])  
    ]
    
beamsLevelThree = [
    (g3, beamsAndPixels[0][0], *beamsAndPixels[0][1]),
	(d4, beamsAndPixels[1][0], *beamsAndPixels[1][1]),
    (fS4, beamsAndPixels[2][0], *beamsAndPixels[2][1]), 
    (g4, beamsAndPixels[3][0], *beamsAndPixels[3][1]), 
    (a4, beamsAndPixels[4][0], *beamsAndPixels[4][1]),
    (d5, beamsAndPixels[5][0], *beamsAndPixels[5][1])
    ]
    
beamsFixed = [
    (g3, beamA, *pixelsA),
	(d4, beamB, *pixelsB),
    (g4, beamC, *pixelsC), 
    (a4, beamD, *pixelsD), 
    (b4, beamE, *pixelsE), 
    (c5, beamF, *pixelsF),
    ]
    
# Lists to hold the solution for each level
solutionLevelOne = [c5, b4, a4, g4]
solutionLevelTwo = [g3, b4, d4, g3, a4, fS4, g4, fS4]
solutionLevelThree = [g3, d4, d5, d4, g3, d4, a4, fS4, g4, fS4, d4, g4, d5, g4, fS4, d4, g4, d5]

# Lists containg tuples to hold the melody notes for each level and assign each one with a duration in seconds and LED pixels
# (Using list as melody contains duplicate notes)
levelOneMelody = [
    (c5, halfNote, *beamsAndPixels[4][1]), 
    (b4, eighthNote, *beamsAndPixels[3][1]),
    (a4, eighthNote, *beamsAndPixels[2][1]),
    (g4, halfNote, *beamsAndPixels[1][1])
    ]
    
levelTwoMelody = [
    (g3, eighthNote, *beamsAndPixels[0][1]), 
    (b4, eighthNote, *beamsAndPixels[5][1]), 
    (d4, eighthNote, *beamsAndPixels[1][1]), 
    (g3, eighthNote, *beamsAndPixels[0][1]),
    (a4, dottedEightNote, *beamsAndPixels[4][1]), 
    (fS4, dottedEightNote, *beamsAndPixels[2][1]),
    (g4, sixteenthNote, *beamsAndPixels[3][1]),
    (fS4, sixteenthNote, *beamsAndPixels[2][1])
    ]
    
levelThreeMelody = [
    (g3, d4, eighthNote, *beamsAndPixels[0][1], *beamsAndPixels[1][1]), 
    (d5, eighthNote, *beamsAndPixels[5][1]), 
    (d4, eighthNote, *beamsAndPixels[1][1]), 
    (g3, eighthNote, *beamsAndPixels[0][1]),
    (d4, a4, dottedEightNote, *beamsAndPixels[1][1], *beamsAndPixels[4][1]), 
    (fS4, dottedEightNote, *beamsAndPixels[2][1]),
    (g4, sixteenthNote, *beamsAndPixels[3][1]), 
    (fS4, sixteenthNote, *beamsAndPixels[2][1]),
    (d4, g4, eighthNote, *beamsAndPixels[1][1], *beamsAndPixels[3][1]), 
    (d5, eighthNote, *beamsAndPixels[5][1]), 
    (g4, sixteenthNote, *beamsAndPixels[3][1]), 
    (fS4, eighthNote, *beamsAndPixels[2][1]),
    (d4, sixteenthNote, *beamsAndPixels[1][1]), 
    (g4, d5, dottedEightNote, *beamsAndPixels[3][1], *beamsAndPixels[5][1]),
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

        elif len(notes) == 5:
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
        
    # Small delay in loop to let user break one or more beams
    # and play one or more notes together
    time.sleep(fixedNoteDelay)
                
    # For loop to turn on LEDs over active beams, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in beamsFixed:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white) 
        
        if beam.is_pressed:
            beamBroken = True
            beamsPlayed.update({note:beam})
            audioOutput.note_on(note, velocity)
            pixels[pixelOne] = (cyan)
            pixels[pixelTwo] = (cyan)
            pixels[pixelThree] = (cyan)
                        
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    if beamBroken == True:
        for note, beam in beamsPlayed.items():
            while beam.is_pressed:
                pass
            # Stop the notes from playing
            audioOutput.note_off(note, velocity)
                	   
    # Reset for next loop through        
    beamBroken = False
    beamsPlayed.clear()

# Function to play notes for level one when beams are broken
def levelOneBeamNotes():
    
    global beamBroken, compareIndex, attemptingPuzzle, matchingNotes, compareIndex, startTime, endTime, beamPressed
        
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    if attemptingPuzzle == False:
        print("Attempt the puzzle...")
        attemptingPuzzle = True
    
    # Small delay in loop to let user break one or more beams
    # and play one or more notes together
    time.sleep(noteDelay)
                
    # For loop to turn on LEDs over active beams, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in beamsLevelOne:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white)  
        
        # When beam is pressed play note and add to list to compare solution
        if beam.is_pressed:
            startTime = time.time()
            beamPressed = True
            beamBroken = True
            beamsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            
            # Turn LEDs red or green depending if note played is correct or incorrect
            if compareIndex <= 3:
                if userSolution[compareIndex] == solutionLevelOne[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
                    
            elif compareIndex > 3:
                pixels[pixelOne] = (red)
                pixels[pixelTwo] = (red)
                pixels[pixelThree] = (red) 
            
            # Increase the index each time beam pressed
            compareIndex += 1
            
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    if beamBroken == True:
        for note, beam in beamsPlayed.items():
            while beam.is_pressed:
                pass
            # Stop the notes from playing
            audioOutput.note_off(note, velocity)
    
    # Check how long since last beam press
    if beamPressed == True:
        endTime = time.time()
        # Calculate length of time note was played
        totalTime = endTime - startTime
        # Reset if more than 15 seconds since last beam press
        if totalTime > resetTime:
            pixels.fill(noColour)
            userSolution.clear()
            matchingNotes = 0
            compareIndex = 0
            startTime = 0
            endTime = 0
            beamPressed = False
            time.sleep(ledFlash)
            print("Puzzle Reset")
                	   
    # Reset for next loop through        
    beamBroken = False
    beamsPlayed.clear() 

# Function to play the level one puzzle    
def levelOnePuzzle():
	
    global matchingNotes, running, compareIndex, completed, firstAttempt, beamPressed
    
    # Play instructions (if required) and melody on first run through
    if firstAttempt == True:
        #instructions()
        playMelodyLevelOne()
        firstAttempt = False
     
    # Recall function to play notes when beams are broken
    levelOneBeamNotes()
    
    # When 4 notes have been played, stop and check if notes are correct
    if len(userSolution) == len(solutionLevelOne):
        # For loop to turn off the lights over active beams
        for note, beam, pixelOne, pixelTwo, pixelThree in beamsLevelOne:
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
        if matchingNotes == 4:
            correctSoundFx()
            print(f"Player got all {matchingNotes} notes correct!")
            applauseSoundFx()
            #congratulations()
            completed = True
            
        elif matchingNotes <= 3:
            wrongSoundFx()
            print(f"Player got {matchingNotes} out of the 4 notes correct.")    
            time.sleep(1)
            print("Try again...")
            attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
        beamPressed = False  
    
    # When more than 4 notes have been played, solution is incorrect       
    elif len(userSolution) > len(solutionLevelOne):
        pixels.fill(noColour)
        print("Checking solution...")
        time.sleep(1)
        
         # For loop to check if lists match
        for index in range(len(solutionLevelOne)):
            if solutionLevelOne[index] == userSolution[index]:
                matchingNotes += 1
        
        # Output how well they did
        wrongSoundFx()
        if matchingNotes < 4:
            print(f"Player got {matchingNotes} out of the 4 notes correct.")
        elif matchingNotes == 4:
            print(f"Player got {matchingNotes} out of the 4 notes correct, but has pressed an extra beam by mistake.")    
        time.sleep(1)
        print("Try again...")
        attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
        beamPressed = False  

# Function to play notes for level two when beams are broken
def levelTwoBeamNotes():
    
    global beamBroken, compareIndex, attemptingPuzzle, matchingNotes, compareIndex, startTime, endTime, beamPressed
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    if attemptingPuzzle == False:
        print("Attempt the puzzle...")
        attemptingPuzzle = True
    
    # Small delay in loop to let user break one or more beams
    # and play one or more notes together
    time.sleep(noteDelay)
                
    # For loop to turn on LEDs over active beams, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in beamsLevelTwo:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white) 
        
        # When beam is pressed play note and add to list to compare solution
        if beam.is_pressed:
            startTime = time.time()
            beamPressed = True
            beamBroken = True
            beamsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            
            # Turn LEDs red or green depending if note played is correct or incorrect
            if compareIndex <= 7:
                if userSolution[compareIndex] == solutionLevelTwo[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
                    
            elif compareIndex > 7:
                pixels[pixelOne] = (red)
                pixels[pixelTwo] = (red)
                pixels[pixelThree] = (red) 
            
            # Increase the index each time beam pressed
            compareIndex += 1
            
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    if beamBroken == True:
        for note, beam in beamsPlayed.items():
            while beam.is_pressed:
                pass
            # Stop the notes from playing
            audioOutput.note_off(note, velocity)
    
    # Check how long since last beam press
    if beamPressed == True:
        endTime = time.time()
        # Calculate length of time note was played
        totalTime = endTime - startTime
        # Reset if more than 15 seconds since last beam press
        if totalTime > resetTime:
            pixels.fill(noColour)
            userSolution.clear()
            matchingNotes = 0
            compareIndex = 0
            startTime = 0
            endTime = 0
            beamPressed = False
            time.sleep(ledFlash)
            print("Puzzle Reset")
                	   
    # Reset for next loop through        
    beamBroken = False
    beamsPlayed.clear() 

# Function to play the level two puzzle    
def levelTwoPuzzle():
	
    global matchingNotes, running, compareIndex, completed, firstAttempt, beamPressed
    
    # Play instructions (if required) and melody on first run through
    if firstAttempt == True:
        #instructions()
        playMelodyLevelTwo()
        firstAttempt = False
         
    # Recall function to play notes when beams are broken
    levelTwoBeamNotes()
    
    # When 8 notes have been played, stop and check if notes are correct
    if len(userSolution) == len(solutionLevelTwo):
        # For loop to turn off the lights over active beams
        for note, beam, pixelOne, pixelTwo, pixelThree in beamsLevelTwo:
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
        if matchingNotes == 8:
            correctSoundFx()
            print(f"Player got all {matchingNotes} notes correct!")
            applauseSoundFx()
            #congratulations()
            completed = True
            
        elif matchingNotes <= 7:
            wrongSoundFx()
            print(f"Player got {matchingNotes} out of the 8 notes correct.")    
            time.sleep(1)
            print("Try again...")
            attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
        beamPressed = False  
    
    # When more than 8 notes have been played, solution is incorrect       
    elif len(userSolution) > len(solutionLevelTwo):
        pixels.fill(noColour)
        print("Checking solution...")
        time.sleep(1)
        
         # For loop to check if lists match
        for index in range(len(solutionLevelTwo)):
            if solutionLevelTwo[index] == userSolution[index]:
                matchingNotes += 1	
        
        # Output how well they did
        wrongSoundFx()
        if matchingNotes < 8:
            print(f"Player got {matchingNotes} out of the 8 notes correct.")
        elif matchingNotes == 8:
            print(f"Player got {matchingNotes} out of the 8 notes correct, but has pressed an extra beam by mistake.")   
        time.sleep(1)
        print("Try again...")
        attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
        beamPressed = False    
        
# Function to play notes for level three when beams are broken
def levelThreeBeamNotes():
    
    global beamBroken, compareIndex, attemptingPuzzle, matchingNotes, compareIndex, startTime, endTime, beamPressed
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    if attemptingPuzzle == False:
        print("Attempt the puzzle...")
        attemptingPuzzle = True
    
    # Small delay in loop to let user break one or more beams
    # and play one or more notes together
    time.sleep(noteDelay)     
           
    # For loop to turn on LEDs over active beams, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in beamsLevelThree:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white) 
        
        # When beam is pressed play note and add to list to compare solution
        if beam.is_pressed:
            startTime = time.time()
            beamPressed = True
            beamBroken = True
            beamsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            
            # Turn LEDs red or green depending if note played is correct or incorrect
            if compareIndex <= 17:
                if userSolution[compareIndex] == solutionLevelThree[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
                    
            elif compareIndex > 17:
                pixels[pixelOne] = (red)
                pixels[pixelTwo] = (red)
                pixels[pixelThree] = (red) 
            
            # Increase the index each time beam pressed
            compareIndex += 1
                        
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    if beamBroken == True:
        for note, beam in beamsPlayed.items():
            while beam.is_pressed:
                pass
            # Stop the notes from playing
            audioOutput.note_off(note, velocity)
    
    # Check how long since last beam press
    if beamPressed == True:
        endTime = time.time()
        # Calculate length of time note was played
        totalTime = endTime - startTime
        # Reset if more than 15 seconds since last beam press
        if totalTime > resetTime:
            pixels.fill(noColour)
            userSolution.clear()
            matchingNotes = 0
            compareIndex = 0
            startTime = 0
            endTime = 0
            beamPressed = False
            time.sleep(ledFlash)
            print("Puzzle Reset")
                	   
    # Reset for next loop through        
    beamBroken = False
    beamsPlayed.clear() 

# Function to play the level three puzzle    
def levelThreePuzzle():
	
    global matchingNotes, running, compareIndex, completed, firstAttempt, beamPressed
    
    # Play instructions (if required) and melody on first run through
    if firstAttempt == True:
        #instructions()
        playMelodyLevelThree()
        firstAttempt = False
	
    # Recall function to play notes when beams are broken
    levelThreeBeamNotes()
    
    # When than 18 notes have been played, stop and check if notes are correct
    if len(userSolution) == len(solutionLevelThree):
        # For loop to turn off the lights over active beams
        for note, beam, pixelOne, pixelTwo, pixelThree in beamsLevelThree:
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
        if matchingNotes == 18:
            correctSoundFx()
            print(f"Player got all {matchingNotes} notes correct!")
            applauseSoundFx()
            #congratulations()
            completed = True
            
        elif matchingNotes <= 17:
            wrongSoundFx()
            print(f"Player got {matchingNotes} out of the 18 notes correct.")    
            time.sleep(1)
            print("Try again...")
            attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
        beamPressed = False
    
    # When more than 18 notes have been played, solution is incorrect        
    elif len(userSolution) > len(solutionLevelThree):
        pixels.fill(noColour)
        print("Checking solution...")
        time.sleep(1)
        
         # For loop to check if lists match
        for index in range(len(solutionLevelThree)):
            if solutionLevelThree[index] == userSolution[index]:
                matchingNotes += 1	
        
        # Output how well they did
        wrongSoundFx()
        if matchingNotes < 18:
            print(f"Player got {matchingNotes} out of the 18 notes correct.")
        elif matchingNotes == 18:
            print(f"Player got {matchingNotes} out of the 18 notes correct, but has pressed an extra beam by mistake.")   
        time.sleep(1)
        print("Try again...")
        attemptingPuzzle = False
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
        beamPressed = False  
        
# Function to speak the puzzle instructions message  
def instructions():
	print("Instructions playing")
	os.system('echo "Can you fix me, by playing the notes, in the correct, order" | festival --tts')
	time.sleep(1)

# Function to speak the puzzle congratulations message
def congratulations():
    global matchingNotes
    print("Congratulations playing")
    os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
    time.sleep(1)

# Function to turn off the LEDs when the puzzle is stoppped    
def stopPuzzle():
    pixels.fill(noColour)

# Start the puzzle
print("The Wonky Piano is running...")
