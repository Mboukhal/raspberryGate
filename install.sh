#!/bin/bash


NAME='gate'
installPath='/usr/bin/gateRp'

# check permissions
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit 127
fi

#if [ "$1" = "-update" ]; then
#     exit 0
#fi

if [ "$1" = "-rm" ]; then

    echo "Unistalling..."
    rm -rf $installPath
    rm -rf /etc/systemd/system/$NAME.service
    systemctl disable $NAME.service
    systemctl stop $NAME.service

    exit 0
fi

SCRIPT=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")

# install python libraries:
echo "Install python libraries..."
apt update
apt install -y python3.9 python3-pip

python3 -m pip install evdev
python3 -m pip install pyusb
python3 -m pip install pyudev
python3 -m pip install requests
python3 -m pip install python-dotenv
python3 -m pip install watchdog
python3 -m pip install netifaces

# copy project directory:
echo "Copying project directory..."
mkdir -p $installPath
cp -ra $SCRIPT_PATH/. $installPath
chmod +x $installPath/src/main.py
chmod +x $installPath/run.sh
chmod +x $installPath/update.sh
mkdir -p /var/log/$NAME/
mv /var/log/$NAME/$NAME.log /var/log/$NAME/$NAME.log.$(date +"%F_%T").backup &> /dev/null
touch /var/log/$NAME/$NAME.log

# set gate in startup service:
echo "Set gate in startup..."
echo "[Unit]" >> /etc/systemd/system/$NAME.service
echo "Description=$NAME" >> /etc/systemd/system/$NAME.service
echo "After=multi-user.target" >> /etc/systemd/system/$NAME.service
echo "" >> /etc/systemd/system/$NAME.service
echo "[Service]" >> /etc/systemd/system/$NAME.service
echo "Type=idle" >> /etc/systemd/system/$NAME.service
echo "User=root" >> /etc/systemd/system/$NAME.service
echo "Restart=always" >> /etc/systemd/system/$NAME.service
echo "RestartSec=2" >> /etc/systemd/system/$NAME.service
echo "ExecStart=bash $installPath/run.sh" >> /etc/systemd/system/$NAME.service
echo "" >> /etc/systemd/system/$NAME.service
echo "[Install]" >> /etc/systemd/system/$NAME.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/$NAME.service

# Reload systemd:
echo "Reload systemd..."
systemctl daemon-reload

# Enable the service:
echo "Enable the service..."
systemctl enable $NAME.service
systemctl start $NAME.service

