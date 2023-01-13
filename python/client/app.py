# app.py

# also importing the request module
from flask import Flask, flash, render_template, request
import sys,os
import configparser
import dbus

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config['IMAGE_FOLDER'] = os.path.join(os.path.dirname(__file__), "images")
app.config['SECRET_KEY'] = 'fajkhSA7DYinDFN7DFNsdf98UNf'

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../../config/rgb_options.ini')

# Configuration for the matrix
config = configparser.ConfigParser()
config.read(filename)

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

# home route
@app.route("/")
def saved_config():
    # Brightness from config file
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    power = config['DEFAULT']['power']
    refresh_rate = config['DEFAULT']['refresh_rate']
    return render_template('index.html', brightness = brightness, width = width, height = height, power = power, refresh_rate = refresh_rate)

# handling power status
@app.route("/power", methods=["GET", "POST"])
def handle_power():
    power = request.form['power']
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    config.set('DEFAULT', 'power', request.form['power'])
    if power == 'on':
      job = manager.StartUnit('zebra.service', 'replace')
    else:
      job = manager.StopUnit('zebra.service', 'replace')
    return render_template('index.html', brightness = brightness, width = width, height = height, power = power)

# handling form data
@app.route('/brightness', methods=['POST'])
def handle_brightness():
    config.set('DEFAULT', 'brightness', request.form['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    power = config['DEFAULT']['power']
    with open(filename, 'w') as configfile:
        config.write(configfile)
    job = manager.RestartUnit('zebra.service', 'fail')
    return render_template('index.html', brightness = request.form['brightness'], width = width, height = height, power = power)

# handling form data
@app.route('/refresh-rate', methods=['POST'])
def handle_refresh_rate():
    config.set('DEFAULT', 'refresh_rate', request.form['refresh_rate'])
    brightness = int(config['DEFAULT']['brightness'])
    power = config['DEFAULT']['power']
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    with open(filename, 'w') as configfile:
        config.write(configfile)
    job = manager.RestartUnit('zebra.service', 'fail')
    return render_template('index.html', brightness = brightness, width = width, height = height, refresh_rate = int(request.form['refresh_rate']), power = power)

@app.route('/image', methods=['POST'])
def handle_image():
    # check if the post request has the file part
    image = request.files("image")
    image.save(os.path.join(app.config["IMAGE_FOLDER"], "image.png"))
    return "", 200
    # if 'file' not in request.files:
    #     flash('No file part')
    #     return
    # file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    # if file.filename == '':
    #     flash('No selected file')
    #     return
    # if file:
    #     file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)

