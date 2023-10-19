

import asyncio
import websockets
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()


def auth():
    msg = \
        {
            "jsonrpc": "2.0",
            "id": 2515,
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": os.getenv('DERIBIT_KEY'),
                "client_secret": os.getenv('DERIBIT_SECRET')
            }
        }
    return msg


async def call_api():
    async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
       ###############
       # Before sending message, make sure that your connection
       # is authenticated (use public/auth call before)
       ###############
        await websocket.send(json.dumps(auth()))
        await websocket.recv()
        wallet: dict[str, float] = {}
        coins = ["BTC", "ETH", "USDC"]
        for coin in coins:
            msg = \
                {
                    "jsonrpc": "2.0",
                    "id": 2515,
                    "method": "private/get_account_summary",
                    "params": {
                        "currency": coin,
                        "extended": True
                    }
                }

            await websocket.send(json.dumps(msg))
            response = await websocket.recv()
            # print(response)
            info = json.loads(response)
            wallet[coin] = info['result']['equity']
    return wallet

res = asyncio.get_event_loop().run_until_complete(call_api())


