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

def displayImage():
    # Configuration file    
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../config/rgb_options.ini')

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

    default_image = os.path.join(dir, config['DEFAULT']['default_image'])
    print(default_image)
    matrix = RGBMatrix(options = options)

    try:
        response = requests.get(imageURL)
        image = Image.open(BytesIO(response.content))
        image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        matrix.SetImage(image.convert('RGB'))
        time.sleep(1)
    except Exception as e:
        image = Image.open(default_image)
        image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        matrix.SetImage(image.convert('RGB'))
        print(e)
        time.sleep(1)
