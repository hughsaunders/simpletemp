import datetime
import json
import glob
from flask import Flask
import Adafruit_DHT

app = Flask(__name__)

#GPIO pin to use for DHT22 Sensor
DHT_PIN = 22
# Note that a kernel driver is used for dallas, so the pin is selected by kernel param.
# See /boot/config.txt especially w1-gpio, if no pin is specified the default is 7

def readDallas():
    # Sample data
    # 4e 01 55 05 7f a5 81 66 78 : crc=78 YES
    # 4e 01 55 05 7f a5 81 66 78 t=20875
    file=glob.glob('/sys/bus/w1/devices/28*')[0]+"/w1_slave"
    ts = datetime.datetime.now().isoformat()
    with open(file) as f:
        temp=float(f.readlines()[1][29:34])/1000
        return (
            {
                "temp_dallas": {
                    "value": temp,
                    "unit": "celsius",
                    "timestamp": ts
                }
            }
        )

def readDHT():
    DHT_SENSOR = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    ts = datetime.datetime.now().isoformat()
    return (
        {
            "temp_dht": {
                "value": temperature,
                "unit" : "celsius",
                "timestamp": ts
            },
            "humidity_dht": {
                "value": humidity,
                "unit" : "RH Percentage",
                "timestamp": ts
            }
        })

@app.route("/")
def temp():
    dallas = {}
    dht = {}

    try:
        dht = readDHT()
    except Exception as e:
        print(e)

    try:
        dallas = readDallas()
    except Exception as e:
        print(e)

    dallas.update(dht)
    return json.dumps(dallas)
