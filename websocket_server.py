import asyncio
import time
import websockets
import sys
import os
import sqlite3

conn = sqlite3.connect('SENSEHAT.db')

def save_temp(temp, pressure, humidity):
    conn.execute(f"INSERT INTO SENSEHAT (ID,TEMPERATURE, PRESSURE, HUMIDITY) \
      VALUES ({time.time()}, {temp}, {pressure}, {humidity})");
    conn.commit()
    
def read_all():
    cursor = conn.execute("SELECT id, temperature, pressure, humidity from SENSEHAT")
    data = ""
    for row in cursor:
        data = data + f"\n{str(row[0])},{str(row[1])},{str(row[2])},{str(row[3])}"
    return data

# create handler for each connection
async def handler(websocket, path):
    data = await websocket.recv()
    data = data.split(",")
    save_temp(data[0], data[1], data[2])
    await websocket.send("Ok")

if __name__ == '__main__':
    try:
        start_server = websockets.serve(handler, "localhost", 8000)
        print("Server listerning")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print(read_all())
        conn.close()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)