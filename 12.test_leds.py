import board
import neopixel
import time

# Set up NeoPixel strip with GPIO pin 12 and 60 LEDs
pixels = neopixel.NeoPixel(board.D12, 60)

# Light up first led
print("One LED on")
pixels[0] = (255, 0, 0)
pixels.show()
time.sleep(5)

# Light up all LEDs
print("All LEDs on")
pixels.fill((0, 255, 0))
pixels.show()
time.sleep(5)

