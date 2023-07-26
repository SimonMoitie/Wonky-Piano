import board
import neopixel
import time

pinNumber = board.D10
ledCount = 60
brightness = 0.2

# Set up NeoPixel strip with GPIO pin 10 and 60 LEDs
pixels = neopixel.NeoPixel(pinNumber, ledCount, brightness = brightness)

# Light up LED - Red
print("LED one on")
pixels[0] = (255, 0, 0)
time.sleep(3)

# Light up LED - Green
print("LED two on")
pixels[1] = (0, 255, 0)
time.sleep(3)

# Light up LED - Blue
print("LED three on")
pixels[2] = (0, 0, 255)
time.sleep(3)

# Light up LED - Yellow
print("LED four on")
pixels[3] = (255, 255, 0)
time.sleep(3)

# Light up LED - Cyan
print("LED five on")
pixels[4] = (0, 255, 255)
time.sleep(3)

# Light up LED - Pink
print("LED six on")
pixels[5] = (255, 0, 255)
time.sleep(3)

# Light up all LEDs - white
print("All LEDs on")
pixels.fill((255, 255, 255))
time.sleep(3)

# Turn off lights
print("All LEDs off")
pixels.fill((0, 0, 0))

