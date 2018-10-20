import os
import asyncio
import json

import paho.mqtt.client as mqtt
from sense_hat import SenseHat


MQTT_HOST = os.environ['MQTT_HOST']
TEMPERATURE_CORRECTION = float(os.environ.get('TEMPERATURE_CORRECTION', "0"))
HUMIDITY_CORRECTION = float(os.environ.get('HUMIDITY_CORRECTION', "0"))

sense = SenseHat()


async def sensors():
    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_HOST)

    while True:
        temperature = sense.temperature + TEMPERATURE_CORRECTION
        humidity = sense.humidity + HUMIDITY_CORRECTION
        pressure = sense.pressure

        mqtt_client.publish('sensors/inside/temperature', temperature)
        mqtt_client.publish('sensors/inside/humidity', humidity)
        mqtt_client.publish('sensors/inside/pressure', pressure)

        all_sensors = json.dumps(dict(
            t=temperature,
            h=humidity,
            p=pressure))

        mqtt_client.publish('sensors/inside', all_sensors)

        await asyncio.sleep(1)


async def main():
    await asyncio.gather(
        sensors()
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()