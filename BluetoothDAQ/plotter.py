
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
  
plt.close('all')
filename = 'Normal2sensorSerial.csv'
data = pd.read_csv(filename)
time = np.array(data.Time)

# 2 Sensor Plotting
voltages = np.array([np.array(data.voltage0),np.array(data.voltage1)])

resistances = 10/(3.3/(3.3-voltages)-1)

displacements = np.exp((resistances-8.03)/-2.78)

fig,ax1=plt.subplots(1)

ax1.plot(time, displacements[0],label = 'Left') 
ax1.plot(time, displacements[1],label = 'Right')  
ax1.set_ylabel('Displacement (cm)')
ax1.set_xlabel('Time (s)')
ax1.legend(loc = 'upper right') 

ax1.set_title('Normal Breathing') 
plt.show()


# # 4 Sensor Plotting
# voltages = np.array([np.array(data.voltage0),np.array(data.voltage1),np.array(data.voltage2),np.array(data.voltage3)])

# resistances = 10/(3.3/(3.3-voltages)-1)

# displacements = np.exp((resistances-2.7)/-2.6)

# fig,ax1=plt.subplots(1)

# ax1.plot(time, displacements[0],label = 'Back Left') 
# ax1.plot(time, displacements[1],label = 'Front Left')
# ax1.plot(time, displacements[2],label = 'Front Right')  
# ax1.plot(time, displacements[3],label = 'Back Right')    
# ax1.set_ylabel('Displacement (cm)')
# ax1.set_xlabel('Time (s)')
# ax1.legend(loc = 'upper right') 

# ax1.set_title('Normal Breathing') 
# plt.show()