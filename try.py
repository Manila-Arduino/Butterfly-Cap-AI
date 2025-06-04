# Example using Adafruit SSD1306 on Raspberry Pi 5B via I²C

import board
import busio
from adafruit_ssd1306 import SSD1306_I2C

from PIL import Image, ImageDraw, ImageFont
import time

# Initialize I²C bus and SSD1306 OLED (128×64)
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Clear display
oled.fill(0)
oled.show()

# # Create a blank image buffer
# width, height = oled.width, oled.height
# image = Image.new("1", (width, height))
# draw = ImageDraw.Draw(image)
# font = ImageFont.load_default()

# # Draw text
# draw.text((0, 0), "Hello, Pi 5B!", font=font, fill=255)

# # Send buffer to OLED
# oled.image(image)
# oled.show()
time.sleep(5)
