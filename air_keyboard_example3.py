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

# Declare variables
port = 2
instrumentMelody = 30
instrumentBeams = 30
instrumentCorrectFx = 9
instrumentWrongFx = 87
instrumentCrowdFx = 126
velocity = 120
beamBroken = False
running = True
buttonsPlayed = {}
userSolution = []
noteDelay = 0.2
matchingNotes = 0
tempo = 104 # bpm (beats per minute)

# Calculate the length of a whole note (seconds in a minute/tempo)
noteDuration = 60/tempo

# Set up pygame and pygame midi
pygame.init()
pygame.midi.init()

# Set up output port
audioOutput = pygame.midi.Output(port)

# Dictionaries to hold the buttons for each level and map each one with a note
buttonsLevelOne = {
    g3 : buttonA, 
    b3 : buttonC, 
    c4 : buttonD, 
    d4 : buttonE, 
    }
   
buttonsLevelTwo = {
	g3 : buttonA,
    a3 : buttonB,
    b3 : buttonC, 
    c4 : buttonD, 
    d4 : buttonE,  
    e4 : buttonF
    }
    
buttonsLevelThree = {
	g3 : buttonA,
    a3 : buttonB, 
    b3 : buttonC, 
    c4 : buttonD, 
    d4 : buttonE, 
    e4 : buttonF
    }
    
# Lists to hold the solution for each level
solutionLevelOne = [g3, d4, b3, c4, b3, g3, g3]
solutionLevelTwo = [g3, d4, b3, c4, b3, g3, g3, a3, e4, c4, d4, e4, d4, a3, d4]
solutionLevelThree = [g3, g3, d4, g3, b3, a3, c4, g3, b3, g3, g3, a3, a3, e4, c4, a3, d4, c4, e4, a3, d4, a3, a3, d4]

# Lists to hold the melody notes for each level and map each one with a duration in seconds
# (Using list as melody contains duplicate notes)
levelOneMelody = [
    (g3, quarterNote), 
    (d4, halfNote), 
    (b3, semiNote), 
    (c4, quarterNote), 
    (b3, semiNote),
    (g3, quarterNote),
    (g3, wholeNote)
    ]
    
levelTwoMelody = [
    (g3, quarterNote), 
    (d4, halfNote), 
    (b3, semiNote), 
    (c4, quarterNote), 
    (b3, semiNote),
    (g3, quarterNote),
    (g3, halfNote),
    (a3, quarterNote),
    (e4, halfNote),
    (c4, semiNote),
    (d4, quarterNote),
    (e4, semiNote),
    (d4, quarterNote),
    (a3, quarterNote),
    (d4, wholeNote)
    ]

levelThreeMelody = [
    (g3, quarterNote), 
    (g3, d4, halfNote), 
    (g3, b3, semiNote), 
    (a3, c4, quarterNote), 
    (g3, b3, semiNote),
    (g3, quarterNote),
    (g3, halfNote),
    (a3, quarterNote),
    (a3, e4, halfNote),
    (c4, semiNote),
    (a3, d4, quarterNote),
    (c4, e4, semiNote),
    (a3, d4, quarterNote),
    (a3, quarterNote),
    (a3, d4, wholeNote)
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
    
    if len(userSolution) >= 15:
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
            print("Thanks for playing.")
            running = False
        elif matchingNotes <= 14:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 15 notes correct.")    
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
    
    if len(userSolution) >= 24:
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
            print("Thanks for playing.")
            running = False
        elif matchingNotes >= 25:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 25 notes correct.")    
            time.sleep(1)
            print("Try again...")
        elif matchingNotes <= 23:
            wrongSoundFx()
            print(f"You got {matchingNotes} out of the 24 notes correct.")    
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

# Begin puzzle
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
