import os
import asyncio
import websockets


locked = None
subs = set()

async def notify_subs():
    global locked
    await asyncio.wait([
        sub.send('UNLOCKED' if locked is None else 'LOCKED')
        for sub in subs
    ])

async def lock(websocket, path):
    global locked
    if not websocket in subs:
        print(f'Subscribed: {websocket}')
        subs.add(websocket)
    try:
        while True:
            await websocket.recv()
            print(f'Received request from {websocket}')

            if locked is None:
                print('  Locked')
                locked = websocket
            elif locked is websocket or locked not in subs:
                # Only the person that locked can unlock
                print(' Unlocked')
                locked = None

            await notify_subs()
            await asyncio.sleep(1)
    finally:
        print(f'Unsubscribed: {websocket}')
        # Make sure to release the lock when owner disconnects
        if websocket is locked:
            locked = None
            await notify_subs()
        subs.remove(websocket)

server_runner = websockets.serve(
    lock,
    os.environ.get('OM_HOST', 'localhost'),
    int(os.environ.get('OM_PORT', 8765)), # TODO: This may break on conversion
)
