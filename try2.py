"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-oled
"""

import time
import RPi.GPIO as GPIO
import Adafruit_SSD1306

# GPIO pin configuration for the OLED display
OLED_RESET_PIN = None  # Set to GPIO pin if your display has a reset pin
OLED = Adafruit_SSD1306.SSD1306_128_64(rst=OLED_RESET_PIN)

# Initialize the OLED display
OLED.begin()

# Clear the display
OLED.clear()
OLED.display()

try:
    while True:
        # Clear the display
        OLED.clear()

        # Display "Hello World!" on OLED
        OLED.draw.text((0, 0), "Hello World!", font=None, fill=255)

        # Display on OLED
        OLED.display()

        # Delay for readability
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()
