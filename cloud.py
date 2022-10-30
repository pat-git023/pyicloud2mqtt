import json
import logging
import os
import sched
import time

import paho.mqtt.publish as publish
from pyicloud import PyiCloudService

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)
time.strftime("%X %x %Z")
os.environ["TZ"] = "Europe/Berlin"

icloudAccount = os.environ["ICLOUD_ACCOUNT"]
icloudPassword = os.environ["ICLOUD_PASS"]
mqtt_hostname= os.environ["MQTT_HOSTNAME"]
mqtt_port = os.environ["MQTT_PORT"]
mqtt_user = os.environ["MQTT_USER"]
mqtt_pass = os.environ["MQTT_PASS"]

mqtt_auth = {}
if mqtt_user:
    mqtt_auth["username"]=mqtt_user
    mqtt_auth["password"]=mqtt_pass
else:
    mqtt_auth = None

s = sched.scheduler(time.time, time.sleep)

api = PyiCloudService(icloudAccount, icloudPassword, "cookiedir", client_id="openhab")

def post_device_updates(sc):
    for i, device in enumerate(api.devices):
        mydevice = {}
        print("My time " + str(time.time()))
        mydevice["id"] = device.data["id"]
        mydevice["batteryLevel"] = device.data["batteryLevel"]
        mydevice["batteryStatus"] = device.data["batteryStatus"]
        mydevice["name"] = device.data["name"]
        mydevice["location"] = device.data["location"]
        publish.single("test/" + mydevice["name"], json.dumps(mydevice, indent=2), hostname=mqtt_hostname, port=mqtt_port, auth=mqtt_auth)
    sc.enter(60, 1, post_device_updates, (sc,))


s.enter(5, 1, post_device_updates, (s,))
try:
    s.run()
except (RuntimeError, TypeError, NameError) as err:
    LOGGER.info("stopped execution: %s", err)
