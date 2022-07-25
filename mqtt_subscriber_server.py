import random
import datetime
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from paho.mqtt import client as mqtt_client
from threading import Thread
import sqlite3

conn = sqlite3.connect('SENSEHAT.db')
"""
#ID == UNIX TIME/DATE
conn.execute('''CREATE TABLE SENSEHAT
         (ID INT PRIMARY KEY    NOT NULL,
         TEMPERATURE        REAL    NOT NULL,
         PRESSURE        REAL    NOT NULL,
         HUMIDITY        REAL    NOT NULL);''')
print("Table created successfully")
"""

readings = '0,0,0'
broker = 'broker.emqx.io'
port = 1883
topic = "sensehat/iot/readings"

client_id = f'iot-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

def save_temp(temp, pressure, humidity):
    conn.execute(f"INSERT INTO SENSEHAT (ID,TEMPERATURE, PRESSURE, HUMIDITY) \
      VALUES ({time.time()}, {temp}, {pressure}, {humidity})");
    conn.commit()
    
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global readings
        readings = msg.payload.decode()
        data = readings.split(',')
        #save_temp(float(data[0]), float(data[1]), float(data[2]))
    client.subscribe(topic)
    client.on_message = on_message

def animate(frame, tx, ty, hx, hy, px, py):

    cur_time = datetime.datetime.now().strftime('%H:%M:%S')
    size_limit = 20
    values = [float(value) for value in readings.split(',')]
    #print('readings', values[0], values[1], values[2])
    tx.append(cur_time)
    ty.append(values[0])
    tx = tx[-size_limit:]
    ty = ty[-size_limit:]
    
    hx.append(cur_time)
    hy.append(values[2])
    hx = hx[-size_limit:]
    hy = hy[-size_limit:]
    
    px.append(cur_time)
    py.append(values[1])
    px = px[-size_limit:]
    py = py[-size_limit:]

    ax[0, 1].clear()
    ax[0, 1].set_title('Temperature')
    ax[0, 1].plot(tx, ty)
    
    ax[1, 0].clear()    
    ax[1, 0].set_title('Humidity')
    ax[1, 0].plot(hx, hy)
    
    ax[1, 1].clear()    
    ax[1, 1].set_title('Pressure')
    ax[1, 1].plot(px, py)
    fig.tight_layout()
    
def thread1():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    
def thread2():

    global ax, fig
    fig, ax = plt.subplots(2,2)
    ax[0, 0].axis([0,10,0,10])
    ax[0, 0].text(5, 7, '3805515 IoT Project', verticalalignment='center', horizontalalignment='center',fontsize=20, fontweight='bold', color='red')
    ax[0, 0].text(5, 5, 'Graphical presentaion of\nLive data readings', verticalalignment='center', horizontalalignment='center', color='green', fontsize=15)
    ax[0, 0].set_xticklabels(())
    ax[0, 0].set_yticklabels(())
    ax[0, 1].tick_params('x', labelrotation=45)
    ax[1, 1].tick_params('x', labelrotation=45)
    ax[1, 0].tick_params('x', labelrotation=45)
    tx_data, ty_data = [], []
    hy_data, hx_data = [], []
    py_data, px_data = [], []
    ani = animation.FuncAnimation(fig, animate, fargs=(tx_data, ty_data, hx_data, hy_data, px_data, py_data), interval=1000)
    
    plt.show()

if __name__ == '__main__':

    thread1 = Thread( target=thread1, args=() )
    thread2 = Thread( target=thread2, args=() )
    thread2.start()
    thread1.start()
    
    thread1.join()
    thread2.join()