#!/bin/bash

echo "Ensure packages are installed:"
sudo apt-get install libopenjp2-7 python3-dbus

echo "Installing pillow library:"
pip install pillow --upgrade

echo "Installing flask library:"
pip install flask --upgrade

echo "Installing waitress library:"
pip install waitress --upgrade

install_path=$(pwd)

echo "Downloading rgb-matrix software setup:"
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh

sed -n '/REBOOT NOW?/q;p' < rgb-matrix.sh > rgb-matrix-zebra.sh

echo "Running rgb-matrix software setup:"
sudo bash rgb-matrix-zebra.sh

echo "Removing rgb-matrix setup script:"
sudo rm rgb-matrix.sh
echo "...done"

echo "Removing zebra service if it exists:"
sudo systemctl stop zebra
sudo rm -rf /etc/systemd/system/zebra.*
sudo systemctl daemon-reload
echo "...done"

echo "Creating zebra service:"
sudo cp ./config/zebra.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python ${install_path}/python/client/app.py &" /etc/systemd/system/zebra.service
sudo systemctl daemon-reload
sudo systemctl start zebra
sudo systemctl enable zebra
echo "...done"

echo -n "In order to finish setup a reboot is necessary..."
echo -n "REBOOT NOW? [y/N] "
read
if [[ ! "$REPLY" =~ ^(yes|y|Y)$ ]]; then
        echo "Exiting without reboot."
        exit 0
fi
echo "Reboot started..."
reboot
sleep infinity
