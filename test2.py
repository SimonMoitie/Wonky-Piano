# Import Libraries
from gpiozero import Button

# Set up variabels for GPIO pins
buttonA = Button(15)
buttonB = Button(14)
buttonC = Button(27)
buttonD = Button(17)
buttonE = Button(24)
buttonF = Button(23)

# While loop to output message when beam is broken
while True:
    if buttonA.is_pressed and buttonB.is_pressed:
        print("Beams A and B are pressed")
    elif buttonB.is_pressed and buttonC.is_pressed:
        print("Beams B and C are pressed")
    elif buttonC.is_pressed and buttonD.is_pressed:
        print("Beams C and D are pressed")
    elif buttonD.is_pressed and buttonE.is_pressed:
        print("Beams D and E are pressed")
    elif buttonE.is_pressed and buttonF.is_pressed:
        print("Beams E and F are pressed")
    elif buttonA.is_pressed and buttonC.is_pressed:
        print("Beam A and C are pressed")
    elif buttonA.is_pressed and buttonD.is_pressed:
        print("Beams A and D are pressed")
    elif buttonA.is_pressed and buttonE.is_pressed:
        print("Beams A and E are pressed")
    elif buttonA.is_pressed and buttonF.is_pressed:
        print("Beams A and F are pressed")
    elif buttonB.is_pressed and buttonD.is_pressed:
        print("Beams B and D are pressed")
    elif buttonB.is_pressed and buttonE.is_pressed:
        print("Beam B and E are pressed")
    elif buttonB.is_pressed and buttonF.is_pressed:
        print("Beams B and F are pressed")
    elif buttonC.is_pressed and buttonD.is_pressed:
        print("Beams C and D are pressed")
    elif buttonC.is_pressed and buttonE.is_pressed:
        print("Beams C and E are pressed")
    elif buttonC.is_pressed and buttonF.is_pressed:
        print("Beams C and F are pressed")
    elif buttonD.is_pressed and buttonE.is_pressed:
        print("Beam D and E are pressed")
    elif buttonD.is_pressed and buttonF.is_pressed:
        print("Beams D and F are pressed")
    elif buttonE.is_pressed and buttonF.is_pressed:
        print("Beams E and F are pressed")       
    elif buttonA.is_pressed:
        print("Beam A is pressed")
    elif buttonB.is_pressed:
        print("Beam B is pressed")
    elif buttonC.is_pressed:
        print("Beam C is pressed")
    elif buttonD.is_pressed:
        print("Beam D is pressed")
    elif buttonE.is_pressed:
        print("Beam E is pressed")
    elif buttonF.is_pressed:
        print("Beam F is pressed")
    else:
        print("All beams are connected")