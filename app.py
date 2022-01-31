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

print("""buttons.py - Detect which button has been pressed

This example should demonstrate how to:
 1. set up RPi.GPIO to read buttons,
 2. determine which button has been pressed

Press Ctrl+C to exit!

""")

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ['Next', 'Previous', 'Home', 'Clean']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    if (BUTTONS.index(pin) == 3):
        clean() 
    if (BUTTONS.index(pin) == 0):
        screen_refresh() 
        print("Button press detected on pin: {} label: {}".format(pin, label))


#!/usr/bin/env python3

inky_display = auto(ask_user=False, verbose=True)


colors = ['Black', 'White', 'Green', 'Blue', 'Red', 'Yellow', 'Orange']

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


# Refresh the screen
def screen_refresh():
    # inky_display.set_rotation(180)
    try:
        inky_display.set_border(inky_display.RED)
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

    intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))
    hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35 * scale_size))
    hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, int(16 * scale_size))

    y_top = int(inky_display.height * (5.0 / 10.0))
    y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))
    name = "Hello World"

    # Calculate the positioning and draw the name text

    name_w, name_h = intuitive_font.getsize(name)
    name_x = int((inky_display.width - name_w) / 2)
    name_y = int(y_top + ((y_bottom - y_top - name_h) / 2))
    draw.text((name_x, name_y), name, inky_display.WHITE, font=hanken_bold_font)


    name_w, name_h = intuitive_font.getsize("Welcome to Inky")
    name_x = int((inky_display.width - name_w) / 2)
    name_y = int(y_top + ((y_bottom - y_top - name_h) / 2)) + 40
    draw.text((name_x, name_y), "Welcome to Inky", inky_display.BLUE, font=hanken_medium_font)

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