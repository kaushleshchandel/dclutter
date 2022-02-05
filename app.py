#!/usr/bin/env python3
# Resolution = 600 x 448

from email.headerregistry import ParameterizedMIMEHeader
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
import paho.mqtt.client as mqtt
import os
from collections import namedtuple 

#variables for stocks
stock_new_pizero2w = 0
stock_new_pizerow = 0
stock_new_pi42gb = 0
stock_new_pi44gb = 0
stock_new_pi48gb = 0

stock_old_pizero2w = 0
stock_old_pizerow = 0
stock_old_pi42gb = 0
stock_old_pi44gb = 0
stock_old_pi48gb = 0

#--------------
# Data Format
# automation/money/
#   cc = {total=3000 ,mtd=2000, wtd=500, today=265}
#   cash  = {total=}
#   bills = {upcoming=3500}
#   debt  = {total=20000, mtm=-3000 }
# 
# automation/home/
#   mqttserver = online
#   hassserver = online
#   zigbeeserver = online
#   dbserver = online
#   vpnserver = online


refreshTime = 60
refreshTimeHome = 600
print("Initializing....")


#Initialize the display
inky_display = auto(ask_user=False, verbose=True)
colors = ['Black', 'White', 'Green', 'Blue', 'Red', 'Yellow', 'Orange']

GPIO.setmode(GPIO.BCM) # Set up RPi.GPIO with the "BCM" numbering scheme
LABELS = ['Up', 'Down', 'Home', 'Power']

# Set the Screen R                    solution and scale size
if inky_display.resolution == (400, 300):
    scale_size = 1.2
    padding = 15
    BUTTONS = [26, 19, 13, 6]
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

if inky_display.resolution == (600, 448):
    scale_size = 2.20
    padding = 30
    BUTTONS = [5, 6, 16, 24] # Buttons for Color epaper
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if inky_display.resolution == (250, 122):
    scale_size = 1.30
    padding = -5


#--------------------------------------------
# Even fired when MQTT Connect
#--------------------------------------------
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic to>    client.subscribe("inky/#")

#--------------------------------------------
# the callback function, it will be triggered when receiving messages
#--------------------------------------------
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")


global CurrentScreenMode 
currentScreenMode = 1

tiny_font  = ImageFont.truetype(HankenGroteskBold, int(10 * scale_size))
small_font  = ImageFont.truetype(HankenGroteskBold, int(16 * scale_size))
medium_font = ImageFont.truetype(HankenGroteskBold, int(20 * scale_size))
large_font  = ImageFont.truetype(HankenGroteskBold, int(24 * scale_size))
huge_font  = ImageFont.truetype(HankenGroteskBold, int(24 * scale_size))


#--------------------------------------------
# Draw the background based on the Image Mode
#--------------------------------------------
def draw_background(mode, img):

    draw = ImageDraw.Draw(img)
    now = datetime.now()
    current_time = now.strftime(" %a - %b %d, %I:%M %p")
    y_top = int(inky_display.height * (5.0 / 10.0))
    y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))

    time = current_time

    name_y = 2 # int(y_top + ((y_bottom - y_top - name_h) / 2))
    draw.text((0, name_y), time, inky_display.BLACK, font=medium_font)

    if currentScreenMode == 1:
        name_w, name_h = medium_font.getsize("[ MAIN ]")
        name_x = int(inky_display.width - name_w)
        draw.text((name_x, name_y), "[ MAIN ]", inky_display.BLACK, font=medium_font)
    if currentScreenMode == 2:
        name_w, name_h = medium_font.getsize("[ MONEY ]")
        name_x = int(inky_display.width - name_w)
        draw.text((name_x, name_y), "[ MONEY ]", inky_display.BLACK, font=medium_font)
    if currentScreenMode == 3:
        name_w, name_h = medium_font.getsize("[ HOME ]")
        name_x = int(inky_display.width - name_w)
        draw.text((name_x, name_y), "[ HOME ]", inky_display.BLACK, font=medium_font)
    if currentScreenMode == 4:
        name_w, name_h = medium_font.getsize("[ WORK ]")
        name_x = int(inky_display.width - name_w)
        draw.text((name_x, name_y), "[ WORK ]", inky_display.BLACK, font=medium_font)


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


#--------------------------------------------
# Update the Screen based on displa Mode
#--------------------------------------------
def update_screen():
    scale_size = 1.0
    padding = 0

    print("Img")

    # Create a new canvas to draw on
    img = Image.new("P", inky_display.resolution)

    # Draw the background for the screen
    print("Draw background")
    draw_background(currentScreenMode, img)

    print("Show image")
    #Finally show the image
    inky_display.set_image(img)
    inky_display.show()
    print("Done")


# Connect to MQTT to get the latest data
print("Connecting to MQTT....")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send th>client.will_set('inky/status', b'{"status": "Off"}')
# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("10.0.2.201", 1883, 60)

print("Subscribe to topic....")
client.subscribe("automation/#",1)
# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash

print("Update screen....")
update_screen()

print("Start MQTT Loop....")
client.loop_start()

import time
starttime = time.time()
starttimeHome = time.time()

#--------------------------------------------
# Reboot the device
#--------------------------------------------
def reboot(shutdown=False):
    print("Rebooting system")

    # Create a new canvas to draw on
    img = Image.new("P", inky_display.resolution)
    y_top = int(inky_display.height * (5.0 / 10.0))
    y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))
    draw = ImageDraw.Draw(img)
    name_w, name_h = huge_font.getsize("Reboot")    
    name_x = int((inky_display.width - name_w)/2)
    draw.text((name_x, 80), "Reboot", inky_display.BLACK, font=huge_font)
    #Finally show the image
    inky_display.set_image(img)
    inky_display.show()
    if shutdown == False:
        os.system('sudo shutdown -r now')
    else:
        os.system('sudo shutdown now')


#--------------------------------------------
# MAIN LOOP
#--------------------------------------------
while True: # Run forever
    #Handle button Press events
    if GPIO.input(BUTTONS[0]) == GPIO.HIGH: # Screen Up button
        print("button A")
        time.sleep(1)
        if currentScreenMode < 2:
            currentScreenMode = 4
        else:
            currentScreenMode = currentScreenMode - 1
        update_screen()
    if GPIO.input(BUTTONS[1]) == GPIO.HIGH: # Screen Down button
        print("button B")
        time.sleep(1)
        if currentScreenMode > 3:
            currentScreenMode = 1
        else:
            currentScreenMode = currentScreenMode + 1
        update_screen()
    if GPIO.input(BUTTONS[2]) == GPIO.HIGH:
        print("button C")
        time.sleep(1)
    if GPIO.input(BUTTONS[3]) == GPIO.HIGH:
        reboot(False)
        print("button D")
        time.sleep(1)
    
    time.sleep(0.1)

    ### This will be updated every loop
    remaining = refreshTime + starttime - time.time()
    remaining_homepage = refreshTimeHome + starttimeHome - time.time()

    ### Countdown finished, ending loop
    if remaining <= 0:
        starttime = time.time()
        print("Refresh Screen")
        update_screen()

    if remaining_homepage <= 0:
        starttimeHome = time.time()
        print("Reset to home page")
        currentScreenMode = 1

    # new MQTT Message based Screen refresh
    # Storing what data has chagned 

    # Update how old certain data is



