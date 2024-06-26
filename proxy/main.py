import json

import requests.exceptions
from dotenv import load_dotenv
import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo
import os
from typing import List
load_dotenv()

ports = serial.tools.list_ports.comports()

ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME')
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY')
if ADAFRUIT_IO_USERNAME is None or ADAFRUIT_IO_KEY is None:
    print("Please set ADAFRUIT_IO_USERNAME and ADAFRUIT_IO_KEY in .env")
    exit(1)

HARDWARE_ID = os.getenv('HARDWARE_ID')
if HARDWARE_ID is None:
    print("Please set HARDWARE_ID in .env")
    exit(1)
else:
    print(f"Using hardware ID: {HARDWARE_ID}")

from Adafruit_IO import Client, Feed, Data
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

wind_feed_name = 'kite-wind'
rssi_feed_name = 'rssi'

def get_receiver_port(ports : List[ListPortInfo]):
    for port, desc, hwid in sorted(ports):
        print(f"{port} {desc} {hwid}")
        if hwid.find(HARDWARE_ID) != -1:
            return port
    return None

receiver_port = get_receiver_port(ports)
if receiver_port is None:
    print("Receiver not found")
    exit(1)

# Read one line from serial port
with serial.Serial(receiver_port, 115200, timeout=1) as ser:
    while True:
        line = ser.readline().strip()
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        try:
            wind_data = Data(value=data['wind'])
            aio.create_data(wind_feed_name, wind_data)
            rssi_data = Data(value=data['rssi'])
            aio.create_data(rssi_feed_name, rssi_data)
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
        print(data)
