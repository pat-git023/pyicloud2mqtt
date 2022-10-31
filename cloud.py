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
#os.environ["TZ"] = "Europe/Berlin"

icloudAccount = os.getenv("ICLOUD_ACCOUNT")
icloudPassword = os.getenv("ICLOUD_PASS")
mqtt_hostname= os.getenv("MQTT_HOSTNAME")
mqtt_port = os.getenv("MQTT_PORT", "1883")
mqtt_user = os.getenv("MQTT_USER")
mqtt_pass = os.getenv("MQTT_PASSWORD")
mqtt_basepath = os.getenv("MQTT_BASEPATH", "icloud/")
update_intervall = os.getenv("UPDATE_INTERVAL", "5")

if mqtt_basepath[-1] != '/':
    mqtt_basepath = mqtt_basepath + '/'


mqtt_auth = {}
if mqtt_user:
    mqtt_auth["username"]=mqtt_user
    mqtt_auth["password"]=mqtt_pass
else:
    mqtt_auth = None

s = sched.scheduler(time.time, time.sleep)

api = PyiCloudService(icloudAccount, icloudPassword, "cookiedir")

def post_device_updates(sc):
    for i, device in enumerate(api.devices):
        mydevice = {}
        mydevice["id"] = device.data["id"]
        mydevice["name"] = device.data["name"]
        mydevice["batteryLevel"] = device.data["batteryLevel"]
        mydevice["batteryStatus"] = device.data["batteryStatus"]
        mydevice["lowPowerMode"] = device.data["lowPowerMode"]
        mydevice["location"] = device.data["location"]
        mydevice["location"]["location"] = str(device.data["location"]["latitude"]) + "," + str(device.data["location"]["longitude"])
        mydevice["deviceModel"] = device.data["deviceModel"]
        mydevice["deviceStatus"] = device.data["deviceStatus"]
        mydevice["deviceDiscoveryId"] = device.data["deviceDiscoveryId"]
        mydevice["baUUID"] = device.data["baUUID"]
        mydevice["rawDeviceModel"] = device.data["rawDeviceModel"]

        # send icloud data to mqtt broker
        publish.single(mqtt_basepath + mydevice["name"], json.dumps(mydevice, indent=2), hostname=mqtt_hostname, port=int(mqtt_port), auth=mqtt_auth)
    sc.enter(int(update_intervall) * 60, 1, post_device_updates, (sc,))


s.enter(5, 1, post_device_updates, (s,))
try:
    s.run()
except (RuntimeError, TypeError, NameError) as err:
    LOGGER.info("stopped execution: %s", err)
