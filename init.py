import globals
import signal
from inky.auto import auto
from inky.inky_uc8159 import CLEAN
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium

print("Initializing....")
#Initialize the display
inky_display = auto(ask_user=False, verbose=True)
colors = ['Black', 'White', 'Green', 'Blue', 'Red', 'Yellow', 'Orange']

# Set the Screen R                    solution and scale size
if inky_display.resolution == (400, 300):
    scale_size = 1.2
    padding = 25

medium_font = ImageFont.truetype(HankenGroteskBold, int(20 * scale_size))

scale_size = 1.0
padding = 0

img = Image.new("P", inky_display.resolution)

draw = ImageDraw.Draw(img)

draw.text((0, 0), "Initializing...", inky_display.BLACK, font=medium_font)

inky_display.set_image(img)
inky_display.show()