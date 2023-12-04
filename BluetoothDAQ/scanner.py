''' 
    - Find bluetooth device in Mac
    https://medium.com/@protobioengineering/how-to-find-all-bluetooth-le-devices-near-you-with-a-macbook-and-python-3f3cbf6871ab 
'''

# scanner.py

import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)                                            

asyncio.run(main())