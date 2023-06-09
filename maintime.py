# name: maintime.py

import display_init
import logging
from display_init import display_image_and_time
from waveshare_epd import epd3in7
from clear_display import clear_all


try:
    # Specify the image path
    image_path = '/home/pi/foehr_credentials/icons/bg_layout_37.jpg'
    
    #epd = epd3in7.EPD()
    #epd.init(1)
    #epd.Clear(0xFF, 1)
    
    clear_all()
    
    while True:
        display_image_and_time(image_path)

    # Clean up resources
    display_init.cleanup()

except Exception as e:
    logging.error(f"An error occurred: {e}")


except Exception as e:
    logging.error(f"An error occurred: {e}")
