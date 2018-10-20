import os
import asyncio
import json

import paho.mqtt.client as mqtt
from sense_hat import SenseHat


MQTT_HOST = os.environ['MQTT_HOST']
TEMPERATURE_CORRECTION = float(os.environ.get('TEMPERATURE_CORRECTION', "0"))
HUMIDITY_CORRECTION = float(os.environ.get('HUMIDITY_CORRECTION', "0"))

sense = SenseHat()


def set_bg(sense, r, g, b):
    for i in range(0, 8):
        for j in range(0, 8):
            sense.set_pixel(i, j, r, g, b)


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


async def heater():
    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_HOST)

    target = 0

    def on_message(client, user_data, message):
        print("MQTT msg >" + message)
        target = int(message)

        if int(message) == 1:
            set_bg(sense, 0, 0, 0)
        else:
            set_bg(sense, 255, 255, 255)

    mqtt_client.on_message = on_message
    mqtt_client.subscribe('heater/target')

    while True:
        print("> " + str(target))
        mqtt_client.loop()
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(
        sensors(),
        heater()
    )


set_bg(sense, 128, 0, 255)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
