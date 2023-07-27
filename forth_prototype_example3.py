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
g3 = 55
a3 = 57
b3 = 59
c4 = 60
d4 = 62
e4 = 64

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

# Declare variables
port = 2 # Midi audio port number
instrumentMelody = 30 # MIDI instrument number for the melody
instrumentBeams = 30 # MIDI instrument number for the beams
instrumentCorrectFx = 9 # MIDI instrument number for correct sound fx 
instrumentWrongFx = 87 # MIDI instrument number for wrong sound fx 
instrumentCrowdFx = 126 # MIDI instrument number for crowd sound fx 
velocity = 110 # Set MIDI volume level (between 0 and 127)
pinNumber = board.D10 # Set LED strip GPIO pin number
ledCount = 28 # Set number of pixels on LED strip
brightness = 0.2 # Set LED strip brightness level (between 0 and 1)
beamBroken = False
running = True
completed = False
buttonsPlayed = {}
userSolution = []
noteDelay = 0.2
fixedNoteDelay = 0.1
matchingNotes = 0
compareIndex = 0
tempo = 104 # bpm (beats per minute)

# Calculate the length of a whole note (seconds in a minute/tempo)
noteDuration = 60/tempo

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up LED strip
pixels = neopixel.NeoPixel(pinNumber, ledCount, brightness = brightness, auto_write = True)

# Set up LED strip - GPIO pin number, number of LEDs, LED brightness, automatically update colours
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
    (g3, buttonsAndPixels[0][0], *buttonsAndPixels[0][1]), 
    (b3, buttonsAndPixels[2][0], *buttonsAndPixels[2][1]), 
    (c4, buttonsAndPixels[3][0], *buttonsAndPixels[3][1]), 
    (d4, buttonsAndPixels[4][0], *buttonsAndPixels[4][1])
    ]
   
buttonsLevelTwo = [
	(g3, buttonsAndPixels[0][0], *buttonsAndPixels[0][1]),
    (a3, buttonsAndPixels[1][0], *buttonsAndPixels[1][1]),
    (b3, buttonsAndPixels[2][0], *buttonsAndPixels[2][1]), 
    (c4, buttonsAndPixels[3][0], *buttonsAndPixels[3][1]), 
    (d4, buttonsAndPixels[4][0], *buttonsAndPixels[4][1]),  
    (e4, buttonsAndPixels[5][0], *buttonsAndPixels[5][1])
    ]
    
buttonsLevelThree = [
	(g3, buttonsAndPixels[0][0], *buttonsAndPixels[0][1]),
    (a3, buttonsAndPixels[1][0], *buttonsAndPixels[1][1]),
    (b3, buttonsAndPixels[2][0], *buttonsAndPixels[2][1]), 
    (c4, buttonsAndPixels[3][0], *buttonsAndPixels[3][1]), 
    (d4, buttonsAndPixels[4][0], *buttonsAndPixels[4][1]),  
    (e4, buttonsAndPixels[5][0], *buttonsAndPixels[5][1])
    ]
    
buttonsFixed = [
    (g3, buttonA, *pixelsA),
    (a3, buttonB, *pixelsB),
    (b3, buttonC, *pixelsC), 
    (c4, buttonD, *pixelsD), 
    (d4, buttonE, *pixelsE),  
    (e4, buttonF, *pixelsF)
    ]
       
# Lists to hold the solution for each level
solutionLevelOne = [g3, d4, b3, c4, b3, g3, g3]
solutionLevelTwo = [g3, d4, b3, c4, b3, g3, g3, a3, e4, c4, d4, e4, d4, a3, d4]
solutionLevelThree = [g3, g3, d4, g3, b3, a3, c4, g3, b3, g3, g3, a3, a3, e4, c4, a3, d4, c4, e4, a3, d4, a3, a3, d4]

# Lists to hold the melody notes for each level and map each one with a duration in seconds
# (Using list as melody contains duplicate notes)
levelOneMelody = [
    (g3, quarterNote, *buttonsAndPixels[0][1]), 
    (d4, halfNote, *buttonsAndPixels[4][1]), 
    (b3, semiNote, *buttonsAndPixels[2][1]), 
    (c4, quarterNote, *buttonsAndPixels[3][1]), 
    (b3, semiNote, *buttonsAndPixels[2][1]),
    (g3, quarterNote, *buttonsAndPixels[0][1]),
    (g3, wholeNote, *buttonsAndPixels[0][1])
    ]
    
levelTwoMelody = [
    (g3, quarterNote, *buttonsAndPixels[0][1]), 
    (d4, halfNote, *buttonsAndPixels[4][1]), 
    (b3, semiNote, *buttonsAndPixels[2][1]), 
    (c4, quarterNote, *buttonsAndPixels[3][1]), 
    (b3, semiNote, *buttonsAndPixels[2][1]),
    (g3, quarterNote, *buttonsAndPixels[0][1]),
    (g3, halfNote, *buttonsAndPixels[0][1]),
    (a3, quarterNote, *buttonsAndPixels[1][1]),
    (e4, halfNote, *buttonsAndPixels[5][1]),
    (c4, semiNote, *buttonsAndPixels[3][1]),
    (d4, quarterNote, *buttonsAndPixels[4][1]),
    (e4, semiNote, *buttonsAndPixels[5][1]),
    (d4, quarterNote, *buttonsAndPixels[4][1]),
    (a3, quarterNote, *buttonsAndPixels[1][1]),
    (d4, wholeNote, *buttonsAndPixels[4][1])
    ]

levelThreeMelody = [
    (g3, quarterNote, *buttonsAndPixels[0][1]), 
    (g3, d4, halfNote, *buttonsAndPixels[0][1], *buttonsAndPixels[4][1]), 
    (g3, b3, semiNote, *buttonsAndPixels[0][1], *buttonsAndPixels[2][1]), 
    (a3, c4, quarterNote, *buttonsAndPixels[1][1], *buttonsAndPixels[3][1]), 
    (g3, b3, semiNote, *buttonsAndPixels[0][1], *buttonsAndPixels[2][1]),
    (g3, quarterNote, *buttonsAndPixels[0][1]),
    (g3, halfNote, *buttonsAndPixels[0][1]),
    (a3, quarterNote, *buttonsAndPixels[1][1]),
    (a3, e4, halfNote, *buttonsAndPixels[1][1], *buttonsAndPixels[5][1]),
    (c4, semiNote, *buttonsAndPixels[3][1]),
    (a3, d4, quarterNote, *buttonsAndPixels[1][1], *buttonsAndPixels[4][1]),
    (c4, e4, semiNote, *buttonsAndPixels[3][1], *buttonsAndPixels[5][1]),
    (a3, d4, quarterNote, *buttonsAndPixels[1][1], *buttonsAndPixels[4][1]),
    (a3, quarterNote, *buttonsAndPixels[1][1]),
    (a3, d4, wholeNote, *buttonsAndPixels[1][1], *buttonsAndPixels[4][1])
    ]

# Function to play level one Melody
def playMelodyLevelOne():
	# Set the instrument
    audioOutput.set_instrument(instrumentMelody)
    
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
    
    # For loop to iterate through dictonary and play a melody   
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
    
    global beamBroken
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
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
    
    global beamBroken, compareIndex
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
           
    # For loop to turn on beams over active LEDs, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelOne:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white)
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
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
	
    global matchingNotes, running, compareIndex, completed
 	     
    # Recall function to play notes when beams are broken
    levelOneBeamNotes()
    
    # When 7 notes have been played, stop and check if notes are correct 
    if len(userSolution) == 7:
        # For loop to turn off the lights over active beams
        for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelOne:
            pixels[pixelOne] = (noColour)
            pixels[pixelTwo] = (noColour)
            pixels[pixelThree] = (noColour)
        print("Lets check your solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelOne)):
            if solutionLevelOne[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 7:
            correctSoundFx()
            print(f"Well done! You got all {matchingNotes} correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            print("Thanks for playing.\nNow relax and play the beams")
            completed = True
        elif matchingNotes <= 6:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 7 notes correct.")    
            time.sleep(1)
            print("Try again...")
            playMelodyLevelOne()
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
    
    # When more than 7 notes have been played, stop bug from happening and reset     
    elif len(userSolution) > 7:
        print("Lets check your solution...")
        time.sleep(1)
        wrongSoundFx()
        print(f"You got {matchingNotes} out of the 5 notes correct.")    
        time.sleep(1)
        print("Try again...")
        playMelodyLevelOne()
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0  

# Function to play notes for level two when beams are broken
def levelTwoBeamNotes():
    
    global beamBroken, compareIndex
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
           
    # For loop to turn on LEDs over active beams, add each broken beam to new list and start note play
    for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelTwo:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white)
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            if compareIndex <= 14:
                if userSolution[compareIndex] == solutionLevelTwo[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
            elif compareIndex > 14:
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
	
    global matchingNotes, running, compareIndex, completed       
	     
    # Recall function to play notes when beams are broken
    levelTwoBeamNotes()
    
    # When 15 notes have been played, stop and check if notes are correct
    if len(userSolution) == 15:
        # For loop to turn off the lights over active beams
        for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelTwo:
            pixels[pixelOne] = (noColour)
            pixels[pixelTwo] = (noColour)
            pixels[pixelThree] = (noColour)
        print("Lets check your solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelTwo)):
            if solutionLevelTwo[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 15:
            correctSoundFx()
            print(f"Well done! You got all {matchingNotes} correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            print("Thanks for playing.\nNow relax and play the beams")
            completed = True
        elif matchingNotes <= 14:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 15 notes correct.")    
            time.sleep(1)
            print("Try again...")
            playMelodyLevelTwo()
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
    
    # When more than 15 notes have been played, stop bug from happening and reset     
    elif len(userSolution) > 15:
        print("Lets check your solution...")
        time.sleep(1)
        wrongSoundFx()
        print(f"You got {matchingNotes} out of the 5 notes correct.")    
        time.sleep(1)
        print("Try again...")
        playMelodyLevelTwo()
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0  
        
# Function to play notes for level three when beams are broken
def levelThreeBeamNotes():
    
    global beamBroken, compareIndex
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
    
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
           
    # For loop to LEDs on over active beams, add each broken beam to new list and start note play
    for note, beam , pixelOne, pixelTwo, pixelThree in buttonsLevelThree:
        pixels[pixelOne] = (white)
        pixels[pixelTwo] = (white)
        pixels[pixelThree] = (white)
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            if compareIndex <= 23:
                if userSolution[compareIndex] == solutionLevelThree[compareIndex]:
                    pixels[pixelOne] = (green)
                    pixels[pixelTwo] = (green)
                    pixels[pixelThree] = (green)
                else:
                    pixels[pixelOne] = (red)
                    pixels[pixelTwo] = (red)
                    pixels[pixelThree] = (red)
            elif compareIndex > 23:
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
	
    global matchingNotes, running, compareIndex, completed   
	     
    # Recall function to play notes when beams are broken
    levelThreeBeamNotes()
    
    # When 24 notes have been played, stop and check if notes are correct
    if len(userSolution) == 24:
        # For loop to turn off the lights over active beams
        for note, beam, pixelOne, pixelTwo, pixelThree in buttonsLevelThree:
            pixels[pixelOne] = (noColour)
            pixels[pixelTwo] = (noColour)
            pixels[pixelThree] = (noColour)
        print("Lets check your solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelThree)):
            if solutionLevelThree[index] == userSolution[index]:
                matchingNotes += 1	
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 24:
            correctSoundFx()
            print(f"Well done! You got all {matchingNotes} correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            print("Thanks for playing.\nNow relax and play the beams")
            completed = True
        elif matchingNotes <= 23:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 24 notes correct.")    
            time.sleep(1)
            print("Try again...")
            playMelodyLevelThree()
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0
    
    # When more than 24 notes have been played, stop bug from happening and reset     
    elif len(userSolution) > 24:
        print("Lets check your solution...")
        time.sleep(1)
        wrongSoundFx()
        print(f"You got {matchingNotes} out of the 5 notes correct.")    
        time.sleep(1)
        print("Try again...")
        playMelodyLevelThree()
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        compareIndex = 0  

# Function to print puzzle instructions to screen    
def instructions():
	print("The game has started...")
	os.system('echo "Can you fix me, by playing the notes, in the correct, order" | festival --tts')
	print("Listen to the melody and try to play it back!")
	time.sleep(1)
	
# Recall function to print instructions
instructions()

# Recall function to play one of the three melodies
#playMelodyLevelOne()
#playMelodyLevelTwo()
playMelodyLevelThree()

# Begin puzzle
print("Your turn..")

# Main loop - To keep program running
while running:
	
	# Recall function to play one of the three puzzle levels
    while completed == False:
	    #levelOnePuzzle()
	    #levelTwoPuzzle() 
	    levelThreePuzzle()
   
    # Recall function to play the fixed piano when puzzle completed
    fixedPiano() 
        
# Clean up
audioOutput.close()
pygame.midi.quit()
pygame.quit()
