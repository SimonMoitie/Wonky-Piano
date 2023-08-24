# Import Libraries
from gpiozero import Button

# Set up variabels for GPIO pins
buttonA = Button(24)
buttonB = Button(23)
buttonC = Button(27)
buttonD = Button(17)
buttonE = Button(15)
buttonF = Button(14)

# Declare variables
beamBroken = False
running = True
buttonList = []

# Dictionary to hold the buttons and map each one with a name
buttons = {
    "Beam A": buttonA, 
    "Beam B": buttonB, 
    "Beam C": buttonC, 
    "Beam D": buttonD, 
    "Beam E": buttonE,
    "Beam F": buttonF
    }
  
# Function to output messages when beams are broken
def beamMessages():
    
    global beamBroken
    
     # For loop to add each broken beam to new list
    for button, beam in buttons.items():
        if beam.is_pressed:
            beamBroken = True
            #print(button +" is pressed")
            buttonList.append(button)
                    
    # Output message if no beams broken
    if beamBroken == False:
        print("All beams are connected")
    # Output message if one or more beams are broken
    elif beamBroken == True:
        if len(buttonList) == 1:
            print(buttonList[0] +" is broken")
        elif len(buttonList) == 2:
            print(buttonList[0] + " and " +buttonList[1] +" are broken")
        elif len(buttonList) == 3:
            print(buttonList[0] + ", " +buttonList[1], " and " +buttonList[2] +" are broken")
        elif len(buttonList) == 4:
            print(buttonList[0] +", " +buttonList[1] +", " +buttonList[2] + " and " +buttonList[3] + " are broken")
        elif len(buttonList) == 5:
            print(buttonList[0] +", " +buttonList[1] +", " +buttonList[2] +", " +buttonList[3] + " and " +buttonList[4] + " are broken")
        elif len(buttonList) == 6:
            print(buttonList[0] +", " +buttonList[1] +", " +buttonList[2] +", " +buttonList[3] + ", " +buttonList[4] + " and " +buttonList[5] +" are broken")
            
    # Reset for next loop through        
    beamBroken = False
    buttonList.clear()
        
# While loop to keep program running
while running:
    
    # Recall function to output message if beams broken
    beamMessages()
