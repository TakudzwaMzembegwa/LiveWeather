import random
import time

from paho.mqtt import client as mqtt_client
from sense_emu import SenseHat

broker = 'broker.emqx.io'
port = 1883
topic = "sensehat/iot/readings"
client_id = f'iot-mqtt-{random.randint(0, 1000)}'
print(client_id)
username = 'emqx'
password = 'public'

sense = SenseHat()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            print(f"Publishing to topic: <{topic}> has started\n...")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    while True:
        result = client.publish(topic, f'{sense.temp},{sense.pressure},{sense.humidity}')
        if result[0] == 0:
            print(f"Success: Sent message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()
