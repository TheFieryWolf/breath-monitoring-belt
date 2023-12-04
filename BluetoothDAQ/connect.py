# connect.py
'''
    - Connect to bluetooth device in Mac
    https://medium.com/@protobioengineering/how-to-connect-to-a-bluetooth-device-with-a-macbook-and-python-7a14ece6a780
    - Part 1: Getting Data
    https://medium.com/@protobioengineering/how-to-talk-to-bluetooth-devices-with-python-part-1-getting-data-30617bb43985

'''
import numpy as np
import struct
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import asyncio
from bleak import BleakClient
import pandas as pd
import numpy as np
import time

address = "78:77:B8:1B:B8:07"
voltages_characteristic_uuid = "00002a19-0000-1000-8000-00805f9b34fc"


async def main():
    # Connect to the Bluetooth device
    async with BleakClient(address) as client:
        suppers = np.array([])
        timerinos = np.array([])
        supperinos = np.array([])
        i = 0
        timerinorino = 15.0
        ogtimerino = time.time()
        fig, ax = plt.subplots()
        fig.set_tight_layout(True)
        while i < 100:
            datas = await client.read_gatt_char(voltages_characteristic_uuid)
            voltages = [struct.unpack('f', datas[0:4]),
                        struct.unpack('f', datas[4:8]),
                        struct.unpack('f', datas[8:12]),
                        struct.unpack('f', datas[12:16]),
                        struct.unpack('f', datas[16:20])]
            # print(voltages)
            datarino = np.array(voltages).reshape(1,-1)
            if len(suppers) == 0:
                suppers  = datarino
            else:
                suppers = np.concatenate([suppers,datarino])
            # print(byte_to_float(data1),byte_to_float(data2))
            # timerino = np.array([time.time() - ogtimerino]).reshape(1,-1)
            # if len(timerinos) == 0:
            #     timerinos = np.array([timerino]).reshape(1,-1)
            #     supperinos = np.array([supperinos]).reshape(1,-1)
            # else:
            #     timerinos = np.concatenate([timerinos,timerino])
            #     supperinos = np.concatenate([supperinos,timerino])
            
            
            
        
            i += 1 
        for sup in suppers:
            print(sup)
        # savetxt(f'{time.time()}.csv', suppers, delimiter=',') # csv log save
        df = pd.DataFrame(suppers)
        df.columns = ["Time", "voltage0", "voltage1", "voltage2", "voltage3"]
        df.to_csv('test'+str(int(time.time()))+".csv",index=False)



asyncio.run(main())
