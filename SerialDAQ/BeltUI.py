import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from ArduinoDAQ import SerialConnect
import time

sg.theme('DarkAmber')   # Add a touch of color
matplotlib.use("TkAgg")
# draw_figure function
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# Arduino connection
def createArduinoDataFile(values):
    if values[0]=='':
        portName = 'COM3' #(typical Win portName)
    else:
        portName = values[0]
    if values[1]=='':
        baudRate   = 19200
    else:
        baudRate   = int(values[1])
    if values[2]=='':
        dataRate   = 50
    else:
        dataRate   = int(values[2])
    if values[3]=='':
        recordTime = 20
    else:
        recordTime = int(values[3])
    if values[4]=='':
        now = int( time.time() )
        snow = str(now)
        filename = 'test' + snow + '.csv'
    else:
        filename = values[4] + '.csv'
    
    numDataPoints = recordTime * dataRate  # Total number of data points to be saved

    #%% Data lists and Arduino commands
    #----------------------------------------------------------------------
    # Data to read from Arduino file
    #----------------------------------------------------------------------
    dataNames = ['Time', 'voltage0', 'voltage1', 'voltage2', 'voltage3']
    dataTypes = [  '=L',       '=f',       '=f',       '=f',       '=f']

    #---------------------------------------------------------------------- 
    # Command strings that can be sent to Arduino
    #----------------------------------------------------------------------
    rate_c     = 'r' # Data rate command
    stop_c     = 's' # Data rate command


    #%% Command data structures 
    # Set recordTime variable to 10 seconds
    #----------------------------------------------------------------------
    commandTimes = [recordTime] # Time to send command
    commandData  = [0] # Value to send over
    commandTypes = ['s'] # Type of command


    #%% Communication with Arduino
    #----------------------------------------------------------------------
    # Do not edit code below
    #----------------------------------------------------------------------
    # initializes all required variables
    s = SerialConnect(portName, filename, baudRate, dataRate, \
                    dataNames, dataTypes, commandTimes, commandData, commandTypes)
    # Connect to Arduino and send over rate
    s.connectToArduino()

    # Start Recording Data
    print("Recording...")

    # Collect data
    while len(s.dataStore[0]) < numDataPoints:
        s.getSerialData()
        
        s.sendCommand() # send command to arduino if ready
        
        # Print number of seconds that have passed
        if len(s.dataStore[0]) % dataRate == 0:
            print(len(s.dataStore[0]) /dataRate)   

    # Close Arduino connection and save data
    s.close()
    return filename

# plotting stuff
def create2SensorFigure(filename):
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
    return fig

def create4SensorFigure(filename):
    data = pd.read_csv(filename)
    time = np.array(data.Time)
    voltages = np.array([np.array(data.voltage0),np.array(data.voltage1),np.array(data.voltage2),np.array(data.voltage3)])

    resistances = 10/(3.3/(3.3-voltages)-1)

    displacements = np.exp((resistances-2.7)/-2.6)

    fig,ax1=plt.subplots(1)

    ax1.plot(time, displacements[0],label = 'Back Left') 
    ax1.plot(time, displacements[1],label = 'Front Left')
    ax1.plot(time, displacements[2],label = 'Front Right')  
    ax1.plot(time, displacements[3],label = 'Back Right')    
    ax1.set_ylabel('Displacement (cm)')
    ax1.set_xlabel('Time (s)')
    ax1.legend(loc = 'upper right') 
    return fig
    
# Define the window layout
layout = [
    [sg.Text('Enter port (default = COM3)'), sg.InputText()],
    [sg.Text('Enter baud rate (default = 19200)'), sg.InputText()],
    [sg.Text('Enter data rate (default = 50 Hz)'), sg.InputText()],
    [sg.Text('Enter record time (default = 20 sec)'), sg.InputText()],
    [sg.Text('Which belt is being used? (2 or 4 sensor, default = 2)'), sg.InputText()],
    [sg.Text('Enter filename (default = will be based on current time)'), sg.InputText()],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Ok")],
]

# Define window 
window = sg.Window(
    "Data Collection",
    layout,
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)

event, values = window.read()

filename = createArduinoDataFile(values)

if values[4]=='' or values[4]=='2':
    figure = create2SensorFigure(filename)
elif values[4]=='4':
    figure = create4SensorFigure(filename)
else:
    figure = create2SensorFigure(filename)
    
# Add the plot to the window
draw_figure(window["-CANVAS-"].TKCanvas, figure)
event, values = window.read()

window.close()