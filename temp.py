import datetime
import json
from flask import Flask

app = Flask(__name__)


def getTemp():
    # Sample data
    # 4e 01 55 05 7f a5 81 66 78 : crc=78 YES
    # 4e 01 55 05 7f a5 81 66 78 t=20875
    file="/sys/bus/w1/devices/28-03129779979d/w1_slave"
    with open(file) as f:
        temp=float(f.readlines()[1][29:34])/1000
        #temp = 21
        return json.dumps({"temp": temp, 
                           "unit": "celsius",
                           "timestamp":datetime.datetime.now().isoformat()})


@app.route("/")
def temp():
    return getTemp()