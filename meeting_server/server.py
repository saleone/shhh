import asyncio
import websockets


locked = False
subs = set()

async def lock(websocket, path):
    while True:
        if not websocket in subs:
            subs.add(websocket)
        await websocket.recv()
        print('Message')
        global locked
        locked = not locked
        state = 'LOCKED' if locked else 'UNLOCKED'

        try:
            await asyncio.wait([sub.send(state) for sub in subs])
            await asyncio.sleep(1)
        finally:
            subs.remove(websocket)

server_runner = websockets.serve(lock, 'localhost', 8765)
