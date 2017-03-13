
# Connecting via USB OTG
(only when you need to get the wifi working)

    $ ls /dev/tty*
    $ screen /dev/tty.usbmodem1423 115200

# Get on wifi

    $ nmcli device wifi list
    $ sudo nmcli device wifi connect 'Lestats' ifname wlan0
    $ nmcli device status
    $ sudo ifconfig

# SSH-ing into the device
(if on the same wifi)

    $ ssh chip@chip1.local

# installing GPIO library
https://github.com/xtacocorex/CHIP_IO

sudo apt-get update
sudo apt-get install git build-essential python-dev python-pip flex bison chip-dt-overlays -y
sudo pip install CHIP-IO

# Installing OSC library
https://pypi.python.org/pypi/python-osc

pip install pyosc


# Running final build

sudo /usr/bin/python /home/chip/spookyphone/hardware-io/phone_in.py && /usr/bin/pd -nogui -rt /home/chip/spookyphone/patch/main.pd


# Updating init.d service for PHONE IO

sudo cp /home/chip/spookyphone/phoneio.service /etc/systemd/system/phoneio.service

sudo systemctl daemon-reload
sudo systemctl enable phoneio.service
sudo systemctl start phoneio
systemctl status phoneio

# Stopping
sudo systemctl stop phoneio


# Updating init.d service for PATCH

sudo cp spookyphone.service /etc/systemd/system/spookyphone.service
sudo systemctl daemon-reload
sudo systemctl enable spookyphone.service
sudo systemctl start spookyphone
systemctl status spookyphone


# Stopping
sudo systemctl stop spookyphone



169.254.5.61
