#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd3in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

# test 

logging.basicConfig(level=logging.DEBUG)

def clear_all():
    try:
        logging.info("epd3in7 Demo")
        
        epd = epd3in7.EPD()
        logging.info("init and Clear")
        epd.init(0)
        epd.Clear(0xFF, 0)
    
    
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd3in7.epdconfig.module_exit()
        exit()


