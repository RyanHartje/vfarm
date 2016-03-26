#!/usr/bin/python
import serial
import datetime

serial_port = '/dev/ttyAMA0'
ser = serial.Serial(serial_port, 9600, timeout=1)

print("\nCurrent pH: %s\n" % data = ser.read())
