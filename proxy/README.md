# Kite Wind

This project measures wind speed at a remote location using an anemometer and an 
Adafruit Feather LoRa transmitter.  This can sit at the beach with no connectivity.
The unit is solar-powered.

The receiver is a Raspberry Pi 4 with a LoRa receiver.  It receives the data via USB 
serial and sends it off to Adafruit IO.

Current dashboard is here: https://io.adafruit.com/thanosd/dashboards/kite-wind

## How to get this running on the Raspberry Pi

If you can boot up the box, connect to it via Ethernet, 
and then SSH into it, you can get this running easily by 
running `sudo raspi-config` and setting up the WiFi.

If that is not possible, it is fairly easy to setup the image again from another machine.

```bash

1. Install 64-bit Raspberry Pi OS Lite on a Raspberry Pi 3
2. Ensure the SSH setting is turned on.
3. Set a username and password
4. Setup the WiFi username / password
5. SSH into the Raspberry Pi
6. Run the following commands:
```bash
sudo apt-get update
sudo apt-get install git pip
git clone git@github.com:thanosd/kite-wind.git
python -m venv kitewind
source kitewind/bin/activate
pip install -r requirements.txt
```

7. Copy the .env file from 1Password to the root of the Python project
8. Install as a service

Instruction here::
https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f

sudo cp /home/thanos/kite-wind/proxy/kitewind.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/kitewind.service
sudo systemctl daemon-reload
sudo systemctl enable kitewind.service
sudo systemctl start kitewind.service
sudo systemctl status kitewind.service
