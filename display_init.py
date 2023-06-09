# 2nd file display_init.py:

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd3in7
from datetime import datetime
import time
import os
import logging
import RPi.GPIO as GPIO
from API_init import fetch_data_from_Google

#import locale as loc
#loc.setlocale(loc.LC_ALL, 'de_DE.utf8')

# time: show seconds?
sec_ = True

# Set up the GPIO channel
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Initialize the display
epd = epd3in7.EPD()

logging.basicConfig(level=logging.DEBUG)

# time 

# Load the font
font_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_thin = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

font24 = ImageFont.truetype(font_bold, 24)
font28 = ImageFont.truetype(font_bold, 28)
font32 = ImageFont.truetype(font_bold, 32)
font_date = ImageFont.truetype(font_thin, 36)
font_time = ImageFont.truetype(font_thin, 45)


# Prepare a canvas to draw on
Himage = Image.new('1', (epd.width, epd.height), 255)  # 1 bit color


def display_image_and_time(image_path):
    try:
        tide_data = fetch_data_from_Google()
        logging.info("Done fetching data. Storing data now ...")
        time.sleep(5)

        tide1, tide2, time1, time2 = tide_data
        logging.info("Done storing data. Creating image ...")
        time.sleep(5)

        # Resize the image
        img = Image.open(image_path).convert("1")  # Convert image to 1 bit color
        #img = img.resize((20, epd.height), Image.ANTIALIAS)
        logging.info("Done resizing image.")
        time.sleep(5)

        # Clear the display
        epd.init(1)  # 1 Gray mode
        epd.Clear(0xFF, 1)
        logging.info("Done clearing display.")
        time.sleep(5)

        # Create a new image with white background
        Himage = Image.new("1", (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(Himage)
        logging.info("Done creating image.")
        time.sleep(5)

        # Paste the resized image onto the white background
        Himage.paste(img, (0, 0))
        draw.text((200, 250), tide1, font=font28, fill=0)
        logging.info("Done pasting image.")
        time.sleep(5)

        # Clear the display
        epd.init(1)  # 1 Gray mode
        epd.Clear(0xFF, 1)
        logging.info("Done clearing display again.")
        time.sleep(5)

        # Display the image
        epd.display_1Gray(epd.getbuffer(Himage))
        logging.info("Done displaying image.")
        time.sleep(5)

        # Update the time
        update_time(show_seconds=sec_)
        logging.info("Done updating time.")
        time.sleep(5)
        
    except Exception as e:
        logging.error(f"Error occurred while displaying image and time: {e}")


def update_time(show_seconds=True):
    while True:
        try:
            logging.info("5.show time, partial update, just 1 Gray mode")
            GPIO.setup(17, GPIO.OUT)  # Set up the GPIO channel for the busy pin (replace 17 with the actual GPIO pin number)
            GPIO.output(17, GPIO.LOW)  # Set the busy pin to low (replace 17 with the actual GPIO pin number)
            epd.init(1)  # 1 Gray mode
            epd.Clear(0xFF, 1)
            time_image = Image.new('1', (epd.width, epd.height), 255)
            time_draw = ImageDraw.Draw(time_image)
            num = 0
            while True:
                time_draw.rectangle((0, 0, epd.width-2, epd.height-2), fill=255)  # Clear the entire image
                if show_seconds==True:
                    time_draw.text((20, 20), time.strftime('%H:%M:%S'), font=font_time, fill=0)
                if show_seconds==False:
                    time_draw.text((20, 20), time.strftime('%H:%M'), font=font_time, fill=0)

                time_draw.text((50, 100), time.strftime('%d. %B %y'), font=font_date, fill=0)

                epd.display_1Gray(epd.getbuffer(time_image))

                #num = num + 1
                #if num == 20:
                    #break

            logging.info("Clear...")
            epd.init(0)  # Initialize the display
            epd.Clear(0xFF, 0)
        except Exception as e:
            logging.error(f"Error occurred while updating time: {e}")

def cleanup():
    try:
        epd.init(0)  # Initialize the display
        epd.Clear(0xFF, 0)  # Clear the display
        epd.sleep()  # Put the display to sleep
    except Exception as e:
        logging.error(f"Error occurred while cleaning up: {e}")
