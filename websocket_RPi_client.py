import asyncio
from websockets import connect, ConnectionClosed
from sense_emu import SenseHat

sense = SenseHat()

async def serv(uri, data):
    async with connect(uri) as websocket:
        await websocket.send(data)
        while(True):
            try:
                resp = await websocket.recv()
                print(resp)
            except ConnectionClosed:
                return
            finally:
                await websocket.close()

while True:
    data = f'{sense.temp},{sense.pressure},{sense.humidity}'
    asyncio.get_event_loop().run_until_complete(serv("ws://localhost:8000", f"{data}"))
#asyncio.run(hello("ws://localhost:8000"))