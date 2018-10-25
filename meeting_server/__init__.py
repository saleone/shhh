import asyncio

from meeting_server.server import server_runner


def run_server():
    asyncio.get_event_loop().run_until_complete(server_runner)
    asyncio.get_event_loop().run_forever()

