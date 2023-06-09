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
sec_ = False

# Set up the GPIO channel
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

row1 = 295
row2 = 380

col1 = 35
col2 = 140

row_clock = 123
row_date = 195

date_format ="%d.%m.%y"

# Initialize the display
epd = epd3in7.EPD()

logging.basicConfig(level=logging.INFO)

# time 

# Load the font
font_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_sans = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_thin = '/home/pi/foehr_credentials/DejaVuSans-ExtraLight.ttf'

font_times = ImageFont.truetype(font_bold, 32)
font_date  = ImageFont.truetype(font_thin, 36)
font_clock = ImageFont.truetype(font_bold, 64)

flut_icon_path = '//home/pi/foehr_credentials/icons/flut.jpg'
ebbe_icon_path = '/home/pi/foehr_credentials/icons/ebbe.jpg'


# Prepare a canvas to draw on
Himage = Image.new('1', (epd.width, epd.height), 255)  # 1 bit color

def display_image_and_time(image_path):
    try:
        tide_data = fetch_data_from_Google()
        logging.info("Done fetching data. Storing data now ...")
        #time.sleep(5)

        tide1, tide2, time1, time2 = tide_data
        logging.info("Done storing data. Creating image ...")
        #time.sleep(5)

        # Background image
        img = Image.open(image_path).convert("1")  # Convert image to 1 bit color
        flut_icon = Image.open(flut_icon_path).convert("1")  # Convert image to 1 bit color
        ebbe_icon = Image.open(ebbe_icon_path).convert("1")  # Convert image to 1 bit color

        logging.info("Done resizing image.")
        #ime.sleep(5)

        # Clear the display
        epd.init(1)  # 1 Gray mode
        epd.Clear(0xFF, 1)
        logging.info("Done clearing display.")
        #time.sleep(5)

        # Create a new image with white background
        Himage = Image.new("1", (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(Himage)
        logging.info("Done creating image.")
        #time.sleep(5)

        # Paste the resized image onto the white background
        Himage.paste(img, (0, 0))
        draw.text((col2, row1+20), time1, font=font_times, fill=0)
        draw.text((col2, row2+20), time2, font=font_times, fill=0)

        print(f"Jetzt ist gerade {tide1}")
        print(f"um {time1} Uhr")

        if tide1 =="Ebbe":
            Himage.paste(ebbe_icon, (col1, row1))
            Himage.paste(flut_icon, (col1, row2))

        if tide1 =="Flut":
            Himage.paste(flut_icon, (col1, row1))
            Himage.paste(ebbe_icon, (col1, row2))

        logging.info("Done pasting image.")
        #time.sleep(5)

        # Clear the display
        epd.init(1)  # 1 Gray mode
        epd.Clear(0xFF, 1)
        logging.info("Done clearing display again.")
        #time.sleep(5)

        # Display the image
        epd.display_1Gray(epd.getbuffer(Himage))
        logging.info("Done displaying image.")
        #time.sleep(5)

        # Update the time
        update_time(critical_time=time1, show_seconds=sec_)
        logging.info("Done updating time.")
        #time.sleep(5)

        return(time1)
        
    except Exception as e:
        logging.error(f"Error occurred while displaying image and time: {e}")


def update_time(show_seconds=True,critical_time=datetime.now()):
    while True:
        try:
            logging.info("5.show time, partial update, just 1 Gray mode")
            GPIO.setup(17, GPIO.OUT)  # Set up the GPIO channel for the busy pin (replace 17 with the actual GPIO pin number)
            GPIO.output(17, GPIO.LOW)  # Set the busy pin to low (replace 17 with the actual GPIO pin number)
            epd.init(1)  # 1 Gray mode
            epd.Clear(0xFF, 1)
            time_image = Image.new('1', (epd.width, epd.height), 255)
            time_draw = ImageDraw.Draw(time_image)

            critical_time = datetime.strptime(critical_time, "%H:%M")
            logging.info(f"datetime.now() <= critical_time: {datetime.now() <= critical_time:}") # 

            while datetime.now() <= critical_time: # ehemals while True 
                
                # date
                time_draw.rectangle((0, 0, epd.width-2, epd.height-2), fill=255)  # Clear the entire image
                if show_seconds==True:
                    time_draw.text((col1, row_clock), time.strftime('%H:%M:%S'), font=font_clock, fill=0)
                if show_seconds==False:
                    time_draw.text((col1, row_clock), time.strftime('%H:%M'), font=font_clock, fill=0)

                # date
                time_draw.text((col1, row_date), time.strftime(date_format), font=font_date, fill=0)

                epd.display_1Gray(epd.getbuffer(time_image))

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
