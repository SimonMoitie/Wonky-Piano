# Import Libraries
import pygame
import pygame.midi
import time
from gpiozero import Button

# Set up variables for GPIO pins
buttonA = Button(23)
buttonB = Button(24)
buttonC = Button(14)
buttonD = Button(15)
buttonE = Button(17)
buttonF = Button(27)

# Set up variables for MIDI melody notes
e4 = 64
g4 = 67
d5 = 74
e5 = 76
g5 = 79
a5 = 81
b5 = 83
cS6 = 85 

# Set up variables for Midi beam notes
e1 = 28
g1 = 31
d2 = 38
e2 = 40
g2 = 43
a2 = 45
b2 = 47
cS3 = 49 

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

# Declare variables
port = 2
instrumentMelody = 68
instrumentBeams = 58
instrumentCorrectFx = 9
instrumentWrongFx = 87
instrumentCrowdFx = 126
velocity = 127
beamBroken = False
running = True
buttonsPlayed = {}
userSolution = []
noteDelay = 0.1
matchingNotes = 0
tempo = 82 # bpm (beats per minute)

# Calculate the length of a whole note (seconds in a minute/tempo)
noteDuration = 60/tempo

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up output port
audioOutput = pygame.midi.Output(port)

# Dictionaries to hold the buttons for each level and map each one with a note
buttonsLevelOne = {
    g1 : buttonB, 
    d2 : buttonC, 
    g2 : buttonD, 
    a2 : buttonE, 
    b2 : buttonF
    }
   
buttonsLevelTwo = {
	e1 : buttonA,
    g1 : buttonB, 
    d2 : buttonC, 
    g2 : buttonD, 
    a2 : buttonE, 
    b2 : buttonF
    }
    
buttonsLevelThree = {
	d2 : buttonA,
    e2 : buttonB, 
    g2 : buttonC, 
    a2 : buttonD, 
    b2 : buttonE, 
    cS3 : buttonF
    }
    
# Lists to hold the solution for each level
solutionLevelOne = [a2, b2, g2, g1, d2]
solutionLevelTwo = [a2, b2, g2, g1, d2, d2, d2, g1, g1, d2,d2,e1]
solutionLevelThree = [e2, b2, e2, b2, e2, b2, cS3, a2, a2, a2, d2, a2, b2, g2, g2, g2, d2, d2, g2, g2, d2, d2, e2]

# Lists to hold the melody notes for each level and map each one with a duration in seconds
# (Using list as melody contains duplicate notes)
levelOneMelody = [
    (a5, quarterNote), 
    (b5, quarterNote), 
    (g5, quarterNote), 
    (g4, quarterNote), 
    (d5, wholeNote)
    ]
    
levelTwoMelody = [
    (a5, semiNote),
    (b5, semiNote),
    (g5, semiNote),
    (g4, semiNote),
    (d5, semiNote),
    (d5, semiNote),
    (d5, semiNote),
    (g4, semiNote),
    (g4, semiNote),
    (d5, semiNote),
    (d5, semiNote),
    (e4, semiNote)
    ]

levelThreeMelody = [
    (e5, semiNote),
    (b5, semiNote),
    (e5, semiNote),
    (b5, semiNote),
    (e5, semiNote),
    (b5, semiNote),
    (cS6, semiNote),
    (a5, semiNote),
    (a5, semiNote),
    (a5, semiNote),
    (d5, semiNote),
    (a5, semiNote),
    (b5, semiNote),
    (g5, semiNote),
    (g5, semiNote),
    (g5, semiNote),
    (d5, semiNote),
    (d5, semiNote),
    (g5, semiNote),
    (g5, semiNote),
    (d5, semiNote),
    (d5, semiNote),
    (e5, semiNote)
    ]

# Function to play level one Melody
def playMelodyLevelOne():
	# Set the instrument
    audioOutput.set_instrument(instrumentMelody)
    
    # For loop to iterate through dictonary and play a melody   
    for note, noteLength in levelOneMelody:
	    audioOutput.note_on(note, velocity)
	    time.sleep(noteLength*noteDuration)
	    audioOutput.note_off(note, velocity)	

# Function to play level two Melody
def playMelodyLevelTwo():
	# Set the instrument
    audioOutput.set_instrument(instrumentMelody)
    
    # For loop to iterate through dictonary and play a melody   
    for note, noteLength in levelTwoMelody:
	    audioOutput.note_on(note, velocity)
	    time.sleep(noteLength*noteDuration)
	    audioOutput.note_off(note, velocity)
	    
# Function to play level three Melody
def playMelodyLevelThree():
	# Set the instrument
    audioOutput.set_instrument(instrumentMelody)
    
    # For loop to iterate through dictonary and play a melody   
    for note, noteLength in levelThreeMelody:
	    audioOutput.note_on(note, velocity)
	    time.sleep(noteLength*noteDuration)
	    audioOutput.note_off(note, velocity)

# Function to play the correct sound effect	    
def correctSoundFx():
	# Set the instrument
	audioOutput.set_instrument(instrumentCorrectFx)
	
	# Play the sound effect
	audioOutput.note_on(soundFx1, velocity)
	time.sleep(1)
	audioOutput.note_off(soundFx1, velocity)

# Function to play the incorrect sound effect
def wrongSoundFx():
	
	# Set instrument
	audioOutput.set_instrument(instrumentWrongFx)
	
	# Play the sound effect
	audioOutput.note_on(soundFx2, velocity)
	time.sleep(0.2)
	audioOutput.note_off(soundFx2, velocity)
	time.sleep(0.1)
	audioOutput.note_on(soundFx3, velocity)
	time.sleep(0.5)
	audioOutput.note_off(soundFx3, velocity)
	
def applauseSoundFx():
	
	# Set instrument
	audioOutput.set_instrument(instrumentCrowdFx)	    
	
	# Play the sound effect
	audioOutput.note_on(soundFx4, velocity)
	time.sleep(3)
	audioOutput.note_off(soundFx4, velocity)

# Function to play notes for level one when beams are broken
def levelOneBeamNotes():
    
    global beamBroken
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
           
    # For loop to add each broken beam to new list and start note play
    for note, beam in buttonsLevelOne.items():
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            
    # If no beams broken do nothing
    if beamBroken == False:
        pass
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    elif beamBroken == True:
        for beam in buttonsPlayed.values():
            while beam.is_pressed:
                pass
        
        # Stop the notes from playing
        for note in buttonsPlayed.keys():        
            audioOutput.note_off(note, velocity)
                	   
    # Reset for next loop through        
    beamBroken = False
    buttonsPlayed.clear() 

# Function to play the level one puzzle    
def levelOnePuzzle():
	
    global matchingNotes, running
	
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
     
    # Recall function to play notes when beams are broken
    levelOneBeamNotes()
    
    if len(userSolution) == 5:
        print("Lets check your solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelOne)):
            if solutionLevelOne[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 5:
            correctSoundFx()
            print(f"Well done! You got all {matchingNotes} correct!")
            applauseSoundFx()
            print("Thanks for playing.")
            running = False
        elif matchingNotes <= 4:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 5 notes correct.")    
            time.sleep(1)
            print("Try again...")
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0

# Function to play notes for level two when beams are broken
def levelTwoBeamNotes():
    
    global beamBroken
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
           
    # For loop to add each broken beam to new list and start note play
    for note, beam in buttonsLevelTwo.items():
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            
    # If no beams broken do nothing
    if beamBroken == False:
        pass
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    elif beamBroken == True:
        for beam in buttonsPlayed.values():
            while beam.is_pressed:
                pass
        
        # Stop the notes from playing
        for note in buttonsPlayed.keys():        
            audioOutput.note_off(note, velocity)
                	   
    # Reset for next loop through        
    beamBroken = False
    buttonsPlayed.clear() 

# Function to play the level two puzzle    
def levelTwoPuzzle():
	
    global matchingNotes, running
	
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
     
    # Recall function to play notes when beams are broken
    levelTwoBeamNotes()
    
    if len(userSolution) == 12:
        print("Lets check your solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelTwo)):
            if solutionLevelTwo[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 12:
            correctSoundFx()
            print(f"Well done! You got all {matchingNotes} correct!")
            applauseSoundFx()
            print("Thanks for playing.")
            running = False
        elif matchingNotes <= 11:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 12 notes correct.")    
            time.sleep(1)
            print("Try again...")
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0
        
# Function to play notes for level three when beams are broken
def levelThreeBeamNotes():
    
    global beamBroken
    
    # Set the instrument
    audioOutput.set_instrument(instrumentBeams)
           
    # For loop to add each broken beam to new list and start note play
    for note, beam in buttonsLevelThree.items():
        if beam.is_pressed:
            beamBroken = True
            buttonsPlayed.update({note:beam})
            userSolution.append(note)
            audioOutput.note_on(note, velocity)
            
    # If no beams broken do nothing
    if beamBroken == False:
        pass
    # If beams were broken, check if beam is still broken
    # and pause program while beam still broken
    elif beamBroken == True:
        for beam in buttonsPlayed.values():
            while beam.is_pressed:
                pass
        
        # Stop the notes from playing
        for note in buttonsPlayed.keys():        
            audioOutput.note_off(note, velocity)
                	   
    # Reset for next loop through        
    beamBroken = False
    buttonsPlayed.clear() 

# Function to play the level three puzzle    
def levelThreePuzzle():
	
    global matchingNotes, running
	
    # Small delay in loop to let user break one or more
    # beams and play one or more notes together
    time.sleep(noteDelay)
     
    # Recall function to play notes when beams are broken
    levelThreeBeamNotes()
    
    if len(userSolution) == 23:
        print("Lets check your solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelThree)):
            if solutionLevelThree[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 23:
            correctSoundFx()
            print(f"Well done! You got all {matchingNotes} correct!")
            applauseSoundFx()
            print("Thanks for playing.")
            running = False
        elif matchingNotes <= 22:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 23 notes correct.")    
            time.sleep(1)
            print("Try again...")
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0

# Function to print puzzle instructions to screen    
def instructions():
	print("The game has started...")
	time.sleep(1)
	print("Listen to the melody and try to play it back!")
	time.sleep(1)
	
# Recall function to print instructions
instructions()
# Recall function to play one of the three melodies
#playMelodyLevelOne()
#playMelodyLevelTwo()
playMelodyLevelThree()
print("Your turn..")

# Main loop - To keep program running
while running:
	
	# Recall function to play one of the three puzzle levels
	#levelOnePuzzle()
	#levelTwoPuzzle() 
	levelThreePuzzle()   
        
# Clean up
audioOutput.close()
pygame.midi.quit()
pygame.quit()
