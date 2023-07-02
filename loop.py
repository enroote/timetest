import time
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd3in7
import os
import logging
import RPi.GPIO as GPIO
from API_init import fetch_data_from_Google
from clear_display import clear_all

now = datetime.now()
next_event = [now + timedelta(seconds=60*2*i) for i in range(int((datetime(2024, 6, 30, 23, 0, 0) - now).total_seconds()/(60*2)))]

i = 0


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

image_path = '/home/pi/foehr_credentials/icons/bg_layout_37.jpg'




while True:
    now = datetime.now()
    day_cal = int(now.strftime("%d"))  # defining start day
    
    while True:
        try:

            clear_all()

            print("******************")
            print("getting new data")
            print("******************")

            tide_data = fetch_data_from_Google()
            logging.info("Done fetching data. Storing data now ...")
            #time.sleep(5)

            tide1, tide2, time1, time2, time1full, time2full = tide_data
            logging.info("Done storing data. Creating image ...")
        
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
            
            print(time1full)
            print(time1full)
            print(type(time1full))
            print(time1full)
            
            
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
            
            epd.sleep()  # Put the display into sleep mode
            logging.info("Display sleeps.")

            time.sleep(1)
            print(tide_data[0])
            # Update the time
            # update_time(next_tide_time=tide_data[2] , show_seconds=sec_)
            # logging.info("Done updating time.")
            # time.sleep(5)      
    
            next_event = datetime.strptime(time1full, "%d.%m.%Y %H:%M:%S")
            print(type(next_event))

            print("***********")
            print(now)
            print(next_event)
            print("***********")

            while now < next_event:
                timeleft = round((next_event - now).total_seconds())
            
                print(next_event.strftime("%H:%M"))
                print("waiting for next event in", timeleft, "s")
            
                time.sleep(5)
                now = datetime.now()
            
                print("day_cal:", day_cal)  # starting day
                print("now:", int(now.strftime("%d")))  # today / now
            
                if day_cal != int(now.strftime("%d")):  # checking if day has changed since start
                    break
                
            if day_cal != int(now.strftime("%d")):  # checking if day has changed since start
                print("******************")
                print("******************")
                print("******************")
                print("Neuer Tag")
                print("******************")
                print("******************")
                print("******************")
                break

        except Exception as e:
            logging.error(f"Error occurred while displaying image and time: {e}")
