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

currentScreenMode = 1

BUTTONS = [26, 19, 13, 6]
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# These correspond to buttons A, B, C and D respectively
LABELS = ['Next', 'Previous', 'Home', 'Clean']


def update_screenMode(ScreenMode, value):
    ScreenMode = ScreenMode + value
    if ScreenMode == 5:
        ScreenMode = 1
    if ScreenMode == 0:
        ScreenMode = 4
    


# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    if (BUTTONS.index(pin) == 3):
        clean() 
    if (BUTTONS.index(pin) == 0):
        update_screenMode(currentScreenMode,1)
        print("Button press detected on pin: {} label: {}".format(pin, label))
    if (BUTTONS.index(pin) == 1):
        update_screenMode(currentScreenMode, -1)
        print("Button press detected on pin: {} label: {}".format(pin, label))


# Ccle through teh colors
def cycle():
    for color in range(7):
        print("Color: {}".format(colors[color]))
        for y in range(inky_display.height):
            for x in range(inky_display.width):
                inky.set_pixel(x, y, color)
        inky_display.set_border(color)
        inky_display.show()

# Clean the Screen
def clean():
    for _ in range(1):
        for y in range(inky_display.height - 1):
            for x in range(inky_display.width - 1):
                inky_display.set_pixel(x, y, CLEAN)

        inky_display.show()

inky_display = auto(ask_user=False, verbose=True)
colors = ['Black', 'White', 'Green', 'Blue', 'Red', 'Yellow', 'Orange']


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
    inky_display.set_image(img) 
    inky_display.show() #Clear the image

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


update_screen()


# Refresh the screen
def screen_refresh():
    # inky_display.set_rotation(180)
    try:
        inky_display.set_border(inky_display.BLACK)
    except NotImplementedError:
        pass

    # Figure out scaling for display size

    scale_size = 1.0
    padding = 0

    if inky_display.resolution == (400, 300):
        scale_size = 2.20
        padding = 15

    if inky_display.resolution == (600, 448):
        scale_size = 2.20
        padding = 30

    if inky_display.resolution == (250, 122):
        scale_size = 1.30
        padding = -5


    # Create a new canvas to draw on

    img = Image.new("P", inky_display.resolution)
    draw = ImageDraw.Draw(img)

    # Load the fonts
 
    y_top = int(inky_display.height * (5.0 / 10.0))
    y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))
    name = "Hello World"

    # Calculate the positioning and draw the name text

    name_w, name_h = intuitive_font.getsize(name)
    name_x = int((inky_display.width - name_w) / 2)
    name_y = int(y_top + ((y_bottom - y_top - name_h) / 2))
    draw.text((name_x, name_y), name, inky_display.BLACK, font=small_font)


    name_w, name_h = intuitive_font.getsize("Welcome to Inky")
    name_x = int((inky_display.width - name_w) / 2)
    name_y = int(y_top + ((y_bottom - y_top - name_h) / 2)) + 40
    draw.text((name_x, name_y), "Welcome to Inky", inky_display.BLACK, font=small_font)

    # Display the completed name badge

    inky_display.set_image(img)
    inky_display.show()




# Refresh the screen
def screen_balance():
     # inky_display.set_rotation(180)
    try:
        inky_display.set_border(inky_display.BLACK)
    except NotImplementedError:
        pass

    # Figure out scaling for display size

    scale_size = 1.0
    padding = 0

    if inky_display.resolution == (400, 300):
        scale_size = 1.2
        padding = 15

    if inky_display.resolution == (600, 448):
        scale_size = 2.20
        padding = 30

    if inky_display.resolution == (250, 122):
        scale_size = 1.30
        padding = -5

    # Create a new canvas to draw on

    img = Image.new("P", inky_display.resolution)
    draw = ImageDraw.Draw(img)

    # Load the fonts

    intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))
    hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35 * scale_size))
    hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, int(16 * scale_size))


# Cash  :  
# Bills :
# Cards : 
# Trend : Good
# Today : 
# Week : 
# Month : 


    bills = "$2500"
    cash = "$3000"
    cards = "$1000"
    trend = "Good"
    today = "$250"
    week = "$1500"
    month = "$3500"

    y_top = 10
    y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))


    # Calculate the positioning and draw the name text

    draw.text((10, 0), "Bills", inky_display.BLACK, font=hanken_bold_font)
    draw.text((10, 50), "Cash", inky_display.BLACK, font=hanken_bold_font)
    draw.text((10, 100), "Cards", inky_display.BLACK, font=hanken_bold_font)
    draw.text((10, 150), "Trend", inky_display.BLACK, font=hanken_bold_font)

    draw.text((10, 200), "TODAY   WEEK   MONTH", inky_display.BLACK, font=intuitive_font)

    draw.text((150, 0), bills, inky_display.BLACK, font=hanken_bold_font)
    draw.text((150, 50), cash, inky_display.BLACK, font=hanken_bold_font)
    draw.text((150, 100), cards, inky_display.BLACK, font=hanken_bold_font)
    draw.text((150, 150), trend, inky_display.BLACK, font=hanken_bold_font)


    # Display the completed name badge

    inky_display.set_image(img)
    inky_display.show()

# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)


# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()