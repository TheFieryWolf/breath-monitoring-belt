/* 
 * ------------------------------------------------------------------------------
 * Reads from an analog channel with time stamping
 * This code is used with Analog_PyArduino_DAQ_Driver.py, which will
 * read serial data and create a data file of (time,voltage)
 * 
 * Version 1.0 (Spring 2022)
 * Comments: To use serial monitor, use the send box and input "f,50"
 * This will output data in serial monitor (free run)
 * To log data, use the Python code above.
 * ------------------------------------------------------------------------------
 */

const int PIN0 = A0;          // Pin use to collect analog data from potenitometer
const int PIN1 = A1;          // Pin use to collect analog data from potenitometer
const int PIN2 = A2;          // Pin use to collect analog data from potenitometer
const int PIN3 = A3;          // Pin use to collect analog data from potenitometer
unsigned long timer = 0;    // used to check current time [microseconds]
long loopTime = 0;       // default time between updates, but will be set in python Code [microseconds]
bool initLooptime = false;  // boolean (T/F) to check if loop time has already been set
bool stopProgram = false;
bool resetTimer = false;

int analogVal0 = 0;          // variable to store potentiometer data [ints]
float voltage0 = 0;          // variable to store potentiometer voltage [V] 

int analogVal1 = 0;          // variable to store potentiometer data [ints]
float voltage1 = 0;          // variable to store potentiometer voltage [V] 

int analogVal2 = 0;          // variable to store potentiometer data [ints]
float voltage2 = 0;          // variable to store potentiometer voltage [V] 

int analogVal3 = 0;          // variable to store potentiometer data [ints]
float voltage3 = 0;          // variable to store potentiometer voltage [V] 

float int2volt = 3.3/1023.0; // Conversion constant from ints to volts [V/int]

void setup() {
  Serial.begin(19200);         // Begin serial comms and set Baud rate
  timer = micros();             // start timer
}
 
void loop() {

  if (Serial.available() > 0) {       // if data is available
    String str = Serial.readStringUntil('\n');
    readFromPC(str); 
  }
  
  if (initLooptime && !stopProgram){ // once loop time has been initialized
    // initLooptime 
    
    timeSync(loopTime);   // sync up time to match data rate
    
    unsigned long currT = micros();  // get current time
  
    analogVal0 = analogRead(PIN0); // get analog data from pin
  
    voltage0 = (float)analogVal0*int2volt; // convert to volts

    analogVal1 = analogRead(PIN1); // get analog data from pin
  
    voltage1 = (float)analogVal1*int2volt; // convert to volts
    
    analogVal2 = analogRead(PIN2); // get analog data from pin
  
    voltage2 = (float)analogVal2*int2volt; // convert to volts
    
    analogVal3 = analogRead(PIN3); // get analog data from pin
  
    voltage3 = (float)analogVal3*int2volt; // convert to volts
  
  
   
    // Send data over serial line to computer
    sendToPC(&currT);
    sendToPC(&voltage0);
    sendToPC(&voltage1);
    sendToPC(&voltage2);
    sendToPC(&voltage3);

  
  }
  else if (initLooptime && stopProgram){
    // also free run
    analogVal0 = analogRead(PIN0); // get analog data from pin
    voltage0 = (float)analogVal0*int2volt; // convert to volts
    analogVal1 = analogRead(PIN1); // get analog data from pin
    voltage1 = (float)analogVal1*int2volt; // convert to volts
    analogVal2 = analogRead(PIN2); // get analog data from pin
    voltage2= (float)analogVal2*int2volt; // convert to volts
    analogVal3 = analogRead(PIN3); // get analog data from pin
    voltage3 = (float)analogVal3*int2volt; // convert to volts
    Serial.print(voltage0);
    Serial.print(" ");
    Serial.print(voltage1);
    Serial.print(" ");
    Serial.print(voltage2);
    Serial.print(" ");
    Serial.print(voltage3);
    Serial.print('\n');
  }

}


/*
 * Timesync calculates the time the arduino needs to wait so it 
 * outputs data at the specified rate
 * Input: deltaT - the data transfer period in microseconds
 */
void timeSync(unsigned long deltaT){
  unsigned long currTime = micros();  // get current time
  long timeToDelay = deltaT - (currTime - timer); // calculate how much time to delay for [us]
  
  if (timeToDelay > 5000) // if time to delay is large 
  {
    // Split up delay commands into delay(milliseconds)
    delay(timeToDelay / 1000);

    // and delayMicroseconds(microseconds)
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0) // If time to delay is positive and small
  {
    // Use delayMicroseconds command
    delayMicroseconds(timeToDelay);
  }
  else
  {
      // timeToDelay is negative or zero so don't delay at all
  }
  timer = currTime + timeToDelay;
}


void readFromPC(const String input){
  int commaIndex = input.indexOf(',');
  char command = input.charAt(commaIndex - 1);
  String data = input.substring(commaIndex + 1);    
  int rate = 0;
  switch(command)
  {
    case 'r':
      // rate command
      rate = data.toInt();
      loopTime = 1000000/rate;         // set loop time in microseconds to 1/frequency sent
      initLooptime = true;             // no longer check for data
      stopProgram = false;
      timer = micros();
      break;
    case 's':
      // stop command
      stopProgram = true;
      initLooptime = false;
      break;
    case 'f':
      // free run
      initLooptime = true;
      stopProgram = true;
      break;
    default:
    // Otherwise, do nothing
      break;
  
  }

}

// ------------------------------------------------------------------------------------------------------------
// Send Data to PC: Methods to send different types of data to PC
// ------------------------------------------------------------------------------------------------------------

void sendToPC(int* data){
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 2);
}

void sendToPC(float* data){
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}
 
void sendToPC(double* data){
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}

void sendToPC(unsigned long* data){
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}
