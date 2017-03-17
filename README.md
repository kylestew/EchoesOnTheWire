
# Connecting via USB OTG
(only when you need to get the wifi working)

    $ ls /dev/tty*
    $ screen /dev/tty.usbmodem1423 115200

# Get on wifi

    $ nmcli device wifi list
    $ sudo nmcli device wifi connect 'Young Hickory WiFi' password 'hotcoffee' ifname wlan0
    sudo nmcli device wifi connect 'Young Hickory WiFi' password 'hotcoffee' ifname wlan0
    $ nmcli device status
    $ sudo ifconfig

# SSH-ing into the device
(if on the same wifi)

    $ ssh chip@chip1.local


# installing Python
Make sure you are on python 3.4 or greater


# installing GPIO library
https://github.com/xtacocorex/CHIP_IO

sudo apt-get update
sudo apt-get install git build-essential python-dev python-pip flex bison chip-dt-overlays -y
sudo pip install CHIP-IO

# Installing OSC library
https://github.com/attwad/python-osc

sudo pip3 install python-osc


# Running final build

sudo /usr/bin/python /home/chip/spookyphone/hardware-io/phone_in.py && /usr/bin/pd -nogui -rt /home/chip/spookyphone/patch/main.pd


# Updating systemd service for PHONE IO

sudo cp /home/chip/spookyphone/phoneio.service /etc/systemd/system/phoneio.service

sudo systemctl daemon-reload
sudo systemctl enable phoneio.service
sudo systemctl start phoneio
systemctl status phoneio

# Stopping
sudo systemctl stop phoneio


# Updating systemd service for PATCH

sudo cp /home/chip/spookyphone/spookyphone.service /etc/systemd/system/spookyphone.service

sudo systemctl daemon-reload
sudo systemctl enable spookyphone.service
sudo systemctl start spookyphone
systemctl status spookyphone


# Stopping
sudo systemctl stop spookyphone
