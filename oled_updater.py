#!/bin/python3

import json
#import time
import sys
from datetime import datetime
#import requests
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

DISPLAY_WIDTH  = 128 
DISPLAY_HEIGHT = 32 

TOP_PADDING = -12
LHS_PADDING = 0
FIRST_LINE_OFFSET = 0
SECOND_LINE_OFFSET = 33

class OledUpdater:

   font_small = ImageFont.truetype("./fonts/OpenSans-Regular.ttf", 10, encoding="unic")
   font_large = ImageFont.truetype("./fonts/OpenSans-Regular.ttf", 30, encoding="unic")

   def __init__(self):
      # Create the I2C interface.
      i2c = busio.I2C(SCL, SDA)

      # width, height, address
      self.display = adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)

      self.clear_display()

      self.image = Image.new("1", (self.display.width, self.display.height))
      self.drawing_obj = ImageDraw.Draw(self.image)

   def clear_display(self):

      # Clear display.
      self.display.fill(0)
      self.display.show()

   def update_display(self, ft_temp, room_temp):
      # Draw a black filled box to clear the image.
      self.drawing_obj.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), outline=0, fill=0)
       
      now = datetime.now()
      dt_string = now.strftime("%d/%m/%y %H:%M:%S")
      print("date and time =", dt_string)

      self.drawing_obj.text((LHS_PADDING, TOP_PADDING + FIRST_LINE_OFFSET), ft_temp + "°C", font=self.font_large, fill=255)
      self.drawing_obj.text((LHS_PADDING, TOP_PADDING + SECOND_LINE_OFFSET), dt_string +"  " + room_temp + "°C", font=self.font_small, fill=255)

      self.display.image(self.image)
      self.display.show()

