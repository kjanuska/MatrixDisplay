import time
import sys
import logging
from logging.handlers import RotatingFileHandler
import requests
from io import BytesIO
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import sys,os
import configparser

def make_square(im, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = 64
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

def displayImage():
    # Configuration file    
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../../config/rgb_options.ini')

    # Configures logger for storing song data    
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='spotipy.log',level=logging.INFO)
    logger = logging.getLogger('zebra-logger')

    # automatically deletes logs more than 2000 bytes
    handler = RotatingFileHandler('zebra.log', maxBytes=2000,  backupCount=3)
    logger.addHandler(handler)

    # Configuration for the matrix
    config = configparser.ConfigParser()
    config.read(filename)

    options = RGBMatrixOptions()
    options.rows = int(config['DEFAULT']['rows'])
    options.cols = int(config['DEFAULT']['columns'])
    options.chain_length = int(config['DEFAULT']['chain_length'])
    options.parallel = int(config['DEFAULT']['parallel'])
    options.hardware_mapping = config['DEFAULT']['hardware_mapping']
    options.gpio_slowdown = int(config['DEFAULT']['gpio_slowdown'])
    options.brightness = int(config['DEFAULT']['brightness'])
    options.limit_refresh_rate_hz = int(config['DEFAULT']['refresh_rate'])

    matrix = RGBMatrix(options = options)

    try:
        while True:
            try:
                image = os.path.join(dir, "images", "image.png")
                image = Image.open(os.path.join(dir, "images", "image.png"))
                image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
                image = make_square(image)
                matrix.SetImage(image.convert('RGB'), unsafe=False)
                time.sleep(1)
            except Exception as e:
                image = Image.open(os.path.join(dir, "images", "zebra.png"))
                image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
                matrix.SetImage(image.convert('RGB'))
                print(e)
                time.sleep(1)
    except Exception as e:
        sys.exit(0)
