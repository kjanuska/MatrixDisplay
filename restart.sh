install_path=$(pwd)

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