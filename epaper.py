import sys
import os

# Waveshare lib imports: 
# Needed to modify the ./lib/waveshare_epd/epdconfig.py as it sets the GPIO.setmode as BCM
# and that conflicts with the rest of this project as it is set to BOARD.
# Make sure to move the lib folder provided by Waveshare to your project root folder,
# and mofify as noted below - I renamed the folder as lib_epaper. Here is a diff of the changes made:
# $ diff epdconfig.py epdconfig.pyORIGINAL
# 40,43c40,43
# <     RST_PIN  = 11
# <     DC_PIN   = 22
# <     CS_PIN   = 24
# <     BUSY_PIN = 18
# ---
# >     RST_PIN  = 17
# >     DC_PIN   = 25
# >     CS_PIN   = 8
# >     BUSY_PIN = 24
# 68c68
# <         self.GPIO.setmode(self.GPIO.BOARD)
# ---
# >         self.GPIO.setmode(self.GPIO.BCM)
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic_epaper')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib_epaper')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd2in7

import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def write_epaper(string1,string2,string3,string4,string5,string6):
    try:

        logging.info("Starting epaper display refresh")
        epd = epd2in7.EPD()

        # '''2Gray(Black and white) display'''
        logging.info("init and Clear")
        epd.init()
        epd.Clear(0xFF)
        
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
        font22 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font26 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 26)
        font28 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 28)
        font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
        font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
        
        # Drawing the stats
        logging.info("1.Drawing the stats horizontally.")
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        
        draw.text((10, 0), string1, font = font22, fill = 0)
        
        draw.line((0, 29, 280, 29), fill = 0) #horizontal line to divide the text fields
        draw.line((0, 30, 280, 30), fill = 0) #horizontal line
        draw.text((10, 30), string2, font = font26, fill = 0)
        draw.line((0, 59, 280, 59), fill = 0) #horizontal line
        draw.line((0, 60, 280, 60), fill = 0) #horizontal line
        draw.text((10, 60), string3, font = font26, fill = 0)
        draw.line((0, 89, 280, 89), fill = 0) #horizontal line
        draw.line((0, 90, 280, 90), fill = 0) #horizontal line
        draw.text((10, 90), string4, font = font26, fill = 0)
        draw.line((0, 119, 280, 119), fill = 0) #horizontal line
        draw.line((0, 120, 280, 120), fill = 0) #horizontal line
        draw.text((10, 120), string5, font = font26, fill = 0)
        draw.line((0, 149, 280, 149), fill = 0) #horizontal line
        draw.line((0, 150, 280, 150), fill = 0) #horizontal line
        draw.text((10, 150), string6, font = font26, fill = 0)


        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd2in7.epdconfig.module_exit()
        exit()