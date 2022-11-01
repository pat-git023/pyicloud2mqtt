# pyicloud2mqtt

pyicloud2mqtt allows you to send data from icloud webservices to a mqtt broker. It is based on the famous [PyiCloud](https://github.com/picklepete/pyicloud) project.  
It just forwards the retrieved data of the connected devices on your iCloud account to an mqtt broker as a JSON document.   

## **!!! Please note that currently no 2FA/2SA authentication is supported !!!**   
Only data (e.g. battery level or location) that is available with user / password authentication will be sent to mqtt.   
Sending data to iCloud is also not supported.

## Requirements
- iCloud credentials
- MQTT broker (e.g. [Eclipse Mosquito](https://mosquitto.org/))
- (optional) Docker 

## Configuration   
The configuration is done via environment variables

### Configuration variables
| env variable | Description | Default | 
| ----------- | ----------- | ----------- |
| ICLOUD_ACCOUNT | your apple id |    | 
| ICLOUD_PASS | your apple password |    |
| MQTT_HOSTNAME | hostname or ip address of your mqtt broker |  |
| MQTT_PORT | port of the mqtt broker | 1883 |
| MQTT_USER | (optional) username for mqtt broker |    |
| MQTT_PASSWORD | (optional) password for mqtt broker |    |
| MQTT_BASEPATH | path of mqtt topic e.g. homeassistant/component | icloud/  |
| UPDATE_INTERVAL | interval in minutes how often the icloud webservices will be called | 5 |

## Usage
You can start it on the commandline:
```bash
pip3 install -r requirements.txt
python3 cloud.py

``` 
or via docker / docker-compose. A simple docker-compose.yml is included. There is an `env_template` file included that can be used.

```bash
cp env_template .env
# change values in .env file
docker-compose up -d
```


