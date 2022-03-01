#!/usr/bin/env python3
# Resolution = 600 x 448

import globals
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
import json
from todoist_api_python.api import TodoistAPI

api = TodoistAPI('1697bd344b2b5fd64e675fa099c7a389ef729637')

print("Initializing....")


#Initialize the display
inky_display = auto(ask_user=False, verbose=True)
colors = ['Black', 'White', 'Green', 'Blue', 'Red', 'Yellow', 'Orange']

GPIO.setmode(GPIO.BCM) # Set up RPi.GPIO with the "BCM" numbering scheme
BUTTON = 26

# Set the Screen R                    solution and scale size
if inky_display.resolution == (400, 300):
    scale_size = 1.2
    padding = 25
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#--------------------------------------------
# Even fired when MQTT Connect
#--------------------------------------------
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic to>    client.subscribe("inky/#")

#--------------------------------------------
# the callback function, it will be triggered when receiving messages

#--------------
# Data Format
# automation/money = {"cash":"6000", "cc":"2500", "debt":"25000", "paid":"1500"}
# automation/home = {"mqtt":"online","hass":"online","zigbee":"online"}
# automation/pistock = {"z2w":"0","zw":"0","42g":"0"}
# automation/uscis = {"status":"New email"}
# automation/emails = {"mip":"2", "me":"20"}
#--------------------------------------------

tiny_font  = ImageFont.truetype(HankenGroteskBold, int(10 * scale_size))
small_font  = ImageFont.truetype(HankenGroteskBold, int(16 * scale_size))
medium_font = ImageFont.truetype(HankenGroteskBold, int(20 * scale_size))
large_font  = ImageFont.truetype(HankenGroteskBold, int(24 * scale_size))
huge_font  = ImageFont.truetype(HankenGroteskBold, int(24 * scale_size))


def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("data Received type",type(m_decode))
    print("data Received",m_decode)
    print("Converting from Json to Object")
    m_in=json.loads(m_decode) #decode json data

    key =topic[11:]
    print("key " + key)

    if key == "money":
        globals.money_cash = int(m_in["cash"])
        globals.money_cc = int(m_in["cc"])
        globals.money_debt = int(m_in["debt"])
        globals.money_paid = globals.total_debt - globals.money_debt
    globals.dataChanged = True


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

    if globals.currentScreenMode == 1:
        name_w, name_h = medium_font.getsize("[ MAIN ]")
        name_x = int(inky_display.width - name_w)
        draw.text((name_x, name_y), "[ MAIN ]", inky_display.BLACK, font=medium_font)
    if globals.currentScreenMode == 2:
        name_w, name_h = medium_font.getsize("[ MONEY ]")
        name_x = int(inky_display.width - name_w)
        draw.text((name_x, name_y), "[ MONEY ]", inky_display.BLACK, font=medium_font)
    if globals.currentScreenMode == 3:
        name_w, name_h = medium_font.getsize("[ HOME ]")
        name_x = int(inky_display.width - name_w)
        draw.text((name_x, name_y), "[ HOME ]", inky_display.BLACK, font=medium_font)
    if globals.currentScreenMode == 4:
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

def show_screen1(img):
    try:
        tasks = api.get_tasks()
        cnt = 0
        for i in tasks:
            cnt += 1
            print(i.content)
            draw = ImageDraw.Draw(img)
            draw.text((10, 50+ cnt*20), str(cnt) + " "  +  str(i.content), inky_display.BLACK, font=small_font)
    except Exception as error:
        print(error)
        draw.text((10, 50+ cnt*20), str(cnt) + " "  +  str(i.content), inky_display.BLACK, font=small_font)


def show_screen2(img):
    print("screen 2")
    draw = ImageDraw.Draw(img)
     #Start drawing the values
    draw.text((0, 50), "Cash", inky_display.BLACK, font=huge_font)
    draw.text((0, 100), "Credit", inky_display.BLACK, font=huge_font)
    draw.text((0, 150), "Debt", inky_display.BLACK, font=huge_font)
    draw.text((0, 200), "Paid", inky_display.BLACK, font=huge_font)


    draw.text((100, 50), str(globals.money_cash), inky_display.BLACK, font=huge_font)
    draw.text((100, 100), str(globals.money_cc), inky_display.BLACK, font=huge_font)
    draw.text((100, 150), str(globals.money_debt), inky_display.BLACK, font=huge_font)
    draw.text((100, 200), str(globals.money_paid), inky_display.BLACK, font=huge_font)

def show_screen3(img):
    print("screen 3")

def show_screen4(img):
    print("screen 4")

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
    draw_background(globals.currentScreenMode, img)

    if globals.currentScreenMode == 1:
        show_screen1(img)
    if globals.currentScreenMode == 2:
        show_screen2(img)
    if globals.currentScreenMode == 3:
        show_screen3(img)
    if globals.currentScreenMode == 4:
        show_screen4(img)

    #Finally show the image
    inky_display.set_image(img)
    inky_display.show()
    globals.dataChanged = False


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
def reboot_shutdown_screen():

    # Create a new canvas to draw on
    img = Image.new("P", inky_display.resolution)
    y_top = int(inky_display.height * (5.0 / 10.0))
    y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))
    draw = ImageDraw.Draw(img)
    name_w, name_h = huge_font.getsize("Hold 5 Sec to reboot")
    name_x = int((inky_display.width - name_w)/2)
    draw.text((name_x, 80), "Hold 5 Sec to reboot", inky_display.BLACK, font=medium_font)
    draw.text((name_x, 110), "Hold 10 Sec to shutdown", inky_display.BLACK, font=medium_font)

    #Finally show the image
    inky_display.set_image(img)
    inky_display.show()


#--------------------------------------------
# Reboot the device
#--------------------------------------------
def reboot(shutdown=False):

    # Create a new canvas to draw on
    img = Image.new("P", inky_display.resolution)
    y_top = int(inky_display.height * (5.0 / 10.0))
    y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))
    draw = ImageDraw.Draw(img)

    if shutdown == False:
        print("Rebooting system")
        name_w, name_h = huge_font.getsize("Reboot")
        name_x = int((inky_display.width - name_w)/2)
        draw.text((name_x, 80), "Reboot", inky_display.BLACK, font=huge_font)
    if shutdown == True:
        print("Shut down system")
        name_w, name_h = huge_font.getsize("Shutdown")
        name_x = int((inky_display.width - name_w)/2)
        draw.text((name_x, 80), "Shutdown", inky_display.BLACK, font=huge_font)

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
    if GPIO.input(BUTTON) == GPIO.HIGH: # Screen Up button
#        print("button A")
        button_pressed_for = 0

        # Write logic here to count how long button is pressed
        while GPIO.input(BUTTON) == GPIO.HIGH:
 #           print("button A Pressed")
            time.sleep(.1)
            button_pressed_for += 1
            if button_pressed_for == 10:
                reboot_shutdown_screen()
            if button_pressed_for > 100: #more than 10 seconds. Shutdown
#                print("button A Short Press  for shutdown")
                reboot(True)

        print("button A Released after " + str(button_pressed_for))
        if button_pressed_for < 10: # Normal Press ccle screen
#            print("button A Short Press")
            if globals.currentScreenMode > 3:
                globals.currentScreenMode = 1
            else:
                globals.currentScreenMode = globals.currentScreenMode + 1
            update_screen()
            time.sleep(.5)

        if button_pressed_for > 40: # Reboot device
#            print("button A Long Press for Reboot")
            reboot(False)

    time.sleep(0.1)

    ### This will be updated every loop
    remaining = globals.refreshTime + starttime - time.time()
    remaining_homepage = globals.refreshTimeHome + starttimeHome - time.time()

    ### Countdown finished, ending loop
    if remaining <= 0:
        starttime = time.time()
        print("Refresh Screen")
#        if globals.dataChanged == True:
        update_screen()

    if remaining_homepage <= 0:
        starttimeHome = time.time()
        print("Reset to home page")
        globals.currentScreenMode = 1
        globals.dataChanged = True

    if globals.dataChanged == True:
        update_screen()
    # Storing what data has chagned

    # Update how old certain data is