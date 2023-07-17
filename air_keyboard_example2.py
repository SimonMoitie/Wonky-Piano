# Import Libraries
import pygame
import pygame.midi
import time
import os
from gpiozero import Button

# Set up variables for GPIO pins
buttonA = Button(23)
buttonB = Button(24)
buttonC = Button(14)
buttonD = Button(15)
buttonE = Button(17)
buttonF = Button(27)

# Set up variables for MIDI melody notes and beams
aS4 = 70
c5 = 72
dS5 = 75
f5 = 77
g5 = 79
aS5 = 82

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
instrumentMelody = 51
instrumentBeams = 51
instrumentCorrectFx = 9
instrumentWrongFx = 87
instrumentCrowdFx = 126
velocity = 127
beamBroken = False
running = True
buttonsPlayed = {}
userSolution = []
noteDelay = 0.25
matchingNotes = 0
tempo = 150 # bpm (beats per minute)

# Calculate the length of a whole note (seconds in a minute/tempo)
noteDuration = 60/tempo

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up output port
audioOutput = pygame.midi.Output(port)

# Dictionaries to hold the buttons for each level and map each one with a note
buttonsLevelOne = {
    c5 : buttonB,
    dS5 : buttonC, 
    f5 : buttonD, 
    g5 : buttonE
    }
   
buttonsLevelTwo = {
	c5 : buttonB,
    dS5 : buttonC, 
    f5 : buttonD, 
    g5 : buttonE, 
    aS5 : buttonF, 
    }
    
buttonsLevelThree = {
    aS4 : buttonA,
	c5 : buttonB,
    dS5 : buttonC, 
    f5 : buttonD, 
    g5 : buttonE, 
    aS5 : buttonF,
    }
    
# Lists to hold the solution for each level
solutionLevelOne = [f5, f5, dS5, f5, g5, c5, dS5]
solutionLevelTwo = [f5, f5, dS5, f5, g5, c5, dS5, aS5, g5, f5, dS5, aS5, g5, f5, dS5, f5]
solutionLevelThree = [c5, f5, c5, f5, dS5, c5, f5, g5, c5, c5, dS5, dS5, aS5, g5, aS4, f5, aS4, dS5, dS5, aS5, g5, aS4, f5, dS5, aS4, f5]

# Lists to hold the melody notes for each level and map each one with a duration in seconds
# (Using list as melody contains duplicate notes)
levelOneMelody = [
    (f5, halfNote), 
    (f5,halfNote), 
    (dS5, semiNote), 
    (f5, semiNote), 
    (g5, quarterNote),
    (c5, quarterNote),
    (dS5, halfNote)
    ]
    
levelTwoMelody = [
    (f5, halfNote), 
    (f5,halfNote), 
    (dS5, semiNote), 
    (f5, semiNote), 
    (g5, quarterNote),
    (c5, quarterNote),
    (dS5, halfNote),
    (aS5, semiNote),
    (g5, quarterNote),
    (f5, quarterNote),
    (dS5, halfNote),
    (aS5, semiNote),
    (g5, quarterNote),
    (f5, quarterNote),
    (dS5, quarterNote),
    (f5, halfNote)    
    ]

levelThreeMelody = [
    (c5, f5, halfNote), 
    (c5, f5,halfNote), 
    (dS5, semiNote), 
    (c5, f5, semiNote), 
    (g5, quarterNote),
    (c5, quarterNote),
    (c5, dS5,halfNote),
    (dS5, aS5, semiNote),
    (g5, quarterNote),
    (aS4, f5, quarterNote),
    (aS4, dS5, halfNote),
    (dS5, aS5, semiNote),
    (g5, quarterNote),
    (aS4, f5, quarterNote),
    (dS5, quarterNote),
    (aS4, f5, halfNote)  
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
    for notes in levelThreeMelody:
		
		# If statement to play single note or two notes together		
        if len(notes) == 3:
            note1, note2, noteLength = notes
            audioOutput.note_on(note1, velocity)
            audioOutput.note_on(note2, velocity)
            time.sleep(noteLength*noteDuration)
            audioOutput.note_off(note1, velocity)
            audioOutput.note_off(note2, velocity)
	    
        if len(notes) == 2:
            note1, noteLength = notes
            audioOutput.note_on(note1, velocity)
            time.sleep(noteLength*noteDuration)
            audioOutput.note_off(note1, velocity)

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
    
    if len(userSolution) >= 7:
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
            print("Thanks for playing.")
            running = False
        elif matchingNotes <= 6:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 7 notes correct.")    
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
    
    if len(userSolution) >= 16:
        print("Lets check your solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelTwo)):
            if solutionLevelTwo[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 16:
            correctSoundFx()
            print(f"Well done! You got all {matchingNotes} correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            print("Thanks for playing.")
            running = False
        elif matchingNotes <= 15:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 16 notes correct.")    
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
    print(len(userSolution))
    if len(userSolution) >= 26:    
        print("Lets check your solution...")
        time.sleep(1)
        
        # For loop to check if lists match
        for index in range(len(solutionLevelThree)):
            if solutionLevelThree[index] == userSolution[index]:
                matchingNotes += 1				
        
        # Output how well they did - end program if all notes correct 
        if matchingNotes == 26:
            correctSoundFx()
            print(f"Well done! You got all {matchingNotes} correct!")
            applauseSoundFx()
            os.system(f'echo "Well done. You have fixed me, by getting all {matchingNotes} notes, in the correct order." | festival --tts')
            print("Thanks for playing.")
            running = False
        elif matchingNotes <= 25:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 26 notes correct.")    
            time.sleep(1)
            print("Try again...")
        
        # Empty list to try again
        userSolution.clear()
        matchingNotes = 0

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
playMelodyLevelTwo()
#playMelodyLevelThree()

# Begin puzzle
print("Your turn..")

# Main loop - To keep program running
while running:
	
	# Recall function to play one of the three puzzle levels
	#levelOnePuzzle()
	levelTwoPuzzle() 
	#levelThreePuzzle()   
        
# Clean up
audioOutput.close()
pygame.midi.quit()
pygame.quit()
