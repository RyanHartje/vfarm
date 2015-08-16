#!/usr/bin/python
import serial
import datetime

serial_port = '/dev/ttyAMA0'
ser = serial.Serial(serial_port, 9600)
# turn on the LEDs
ser.write("L,1\r")
ser.write("C,1\r")
line = ""

while True:
  data = ser.read()
  if(data == "\r"):
    print "Received from sensor:" + line
    line = ""
  else:
    line = line + data

