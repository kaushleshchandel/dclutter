#!/usr/bin/env python3
# Resolution = 600 x 448

import signal
import RPi.GPIO as GPIO
import time
from inky.auto import auto
from inky.inky_uc8159 import CLEAN
import argparse
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from datetime import datetime

global CurrentScreenMode 

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

#BUTTONS = [5, 6, 16, 24] # Buttons for Color epaper
#GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

BUTTONS = [26, 19, 13, 6]
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
LABELS = ['Next', 'Previous', 'Home', 'Clean']

currentScreenMode = 1

def update_screenMode(ScreenMode, value):
    print("Old Screen Mode " + str(ScreenMode))
    ScreenMode = ScreenMode + value
    if ScreenMode == 5:
        ScreenMode = 1
    if ScreenMode == 0:
        ScreenMode = 4
    #update_screen()
    print("New Screen Mode " + str(ScreenMode))
    time.sleep(1)
    return ScreenMode

# Clean the Screen
def clean():
    for _ in range(1):
        for y in range(inky_display.height - 1):
            for x in range(inky_display.width - 1):
                inky_display.set_pixel(x, y, CLEAN)

        inky_display.show()

inky_display = auto(ask_user=False, verbose=True)
colors = ['Black', 'White', 'Green', 'Blue', 'Red', 'Yellow', 'Orange']

# Set the Screen Rsolution and scale size
if inky_display.resolution == (400, 300):
    scale_size = 1.2
    padding = 15

if inky_display.resolution == (600, 448):
    scale_size = 2.20
    padding = 30

if inky_display.resolution == (250, 122):
    scale_size = 1.30
    padding = -5

tiny_font  = ImageFont.truetype(HankenGroteskBold, int(10 * scale_size))
small_font  = ImageFont.truetype(HankenGroteskBold, int(16 * scale_size))
medium_font = ImageFont.truetype(HankenGroteskBold, int(20 * scale_size))
large_font  = ImageFont.truetype(HankenGroteskBold, int(24 * scale_size))
huge_font  = ImageFont.truetype(HankenGroteskBold, int(24 * scale_size))


#Draw the background based on the Image Mode
def draw_background(mode, img):

    draw = ImageDraw.Draw(img)
    #inky_display.set_image(img) 
    #inky_display.show() #Clear the image

    now = datetime.now()
    current_time = now.strftime("%B %d, %I:%M%p")
    y_top = int(inky_display.height * (5.0 / 10.0))
    y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))

    time = current_time
    name_w, name_h = medium_font.getsize(time)
    name_x = int((inky_display.width - name_w) / 2)
    name_y = 2 # int(y_top + ((y_bottom - y_top - name_h) / 2))
    draw.text((name_x, name_y), time, inky_display.BLACK, font=medium_font)

    top_margin = 40

    draw.ellipse((inky_display.width - 15, top_margin + 10, inky_display.width -5 ,top_margin + 20), outline= inky_display.BLACK)
    draw.ellipse((inky_display.width - 15, top_margin + 30, inky_display.width -5 ,top_margin + 40), outline= inky_display.BLACK)
    draw.ellipse((inky_display.width - 15, top_margin + 50, inky_display.width -5 ,top_margin + 60), outline= inky_display.BLACK)
    draw.ellipse((inky_display.width - 15, top_margin + 70, inky_display.width -5 ,top_margin + 80), outline= inky_display.BLACK)
#    draw.ellipse((inky_display.width - 15, top_margin + 90, inky_display.width -5 ,top_margin + 100), outline= inky_display.BLACK)

    if mode == 1:
        draw.ellipse((inky_display.width - 15, top_margin + 10, inky_display.width -5 ,top_margin + 20), fill= inky_display.BLACK)
    if mode == 2:
        draw.ellipse((inky_display.width - 15, top_margin + 30, inky_display.width -5 ,top_margin + 40), fill= inky_display.BLACK)
    if mode == 3:
        draw.ellipse((inky_display.width - 15, top_margin + 50, inky_display.width -5 ,top_margin + 60), fill= inky_display.BLACK)
    if mode == 4:
        draw.ellipse((inky_display.width - 15, top_margin + 70, inky_display.width -5 ,top_margin + 80), fill= inky_display.BLACK)
#    if mode == 5:
#        draw.ellipse((inky_display.width - 15, top_margin + 90, inky_display.width -5 ,top_margin + 100), fill= inky_display.BLACK)


def update_screen():
    scale_size = 1.0
    padding = 0

    # Create a new canvas to draw on
    img = Image.new("P", inky_display.resolution)

    # Draw the background for the screen
    draw_background(currentScreenMode, img)

    #Finally show the image
    inky_display.set_image(img)
    inky_display.show()


while True: # Run forever
    #Handle button Press events
    if GPIO.input(BUTTONS[0]) == GPIO.HIGH: # Screen Up button
        time.sleep(1)
        if currentScreenMode < 2:
            currentScreenMode = 4
        else:
            currentScreenMode = currentScreenMode - 1
        update_screen()
    if GPIO.input(BUTTONS[1]) == GPIO.HIGH: # Screen Down button
        time.sleep(1)
        if currentScreenMode > 3:
            currentScreenMode = 1
        else:
            currentScreenMode = currentScreenMode + 1
        update_screen()
    if GPIO.input(BUTTONS[2]) == GPIO.HIGH:
        time.sleep(1)
    if GPIO.input(BUTTONS[3]) == GPIO.HIGH:
        time.sleep(1)


