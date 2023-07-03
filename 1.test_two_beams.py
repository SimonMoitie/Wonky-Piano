from gpiozero import Button

buttonA = Button(14)
buttonB = Button(15)

while True:
	if buttonA.is_pressed and buttonB.is_pressed:
		print("Beam A and Beam B are pressed")
	elif buttonA.is_pressed:
		print("Beam A is pressed")
	elif buttonB.is_pressed:
		print("Beam B is pressed")
	else:
		print("Beam A and Beam B are connected")

		
