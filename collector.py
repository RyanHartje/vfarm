#!/usr/bin/python
import serial, smtplib, logging, datetime
from mailinglogger.MailingLogger import MailingLogger
from models import ph
#from adjust import alert

handler = MailingLogger('will@solidarray.com',('modestegotist@gmail.com',), flood_level=1)
logger = logging.getLogger()
logger.addHandler(handler)

print('initializing serial')
serial_port = '/dev/ttyAMA0'
ser = serial.Serial(serial_port, 9600)

#  turn on the LEDs
ser.write("L,1\r")
ser.write("C,1\r")

def collect():
    # We'll need to loop through the output given by the probe
    # For this, we need a bool, and an empty string
    print('setting up')
    not_carriage_return = True
    line = ""

    try:
      # Also set up our data point
      ph_now = ph()
    except:
      raise BaseException('Mongo connection failed')
   
    # We need to loop until we see \r
    while not_carriage_return:
      data = ser.read()
      if(data == "\r"):
        print('We be loopin: %s' % line)
        if(not line == "*ER"):
          if float(line) > 7.5:
            logging.error('PH LEVELS TOO HIGH. LOWERING BY %d' % (7.5 - float(line)))
            ph_now['ph'] = float(line)
            not_carriage_return = False
          elif float(line) < 6.5:
            logging.error('PH LEVELS TOO LOW. RAISING BY %d' % (float(line) - 6.5))
            ph_now['ph'] = float(line)
            not_carriage_return = False
          else:
            ph_now['ph'] = float(line)
            not_carriage_return = False
        else:
          line = ""
      else:
        line = line + data

    try:
      ph_now.save()
      print("Recorded PH is: %s" % ph_now['ph'])
      print("Current Time: %s" % datetime.datetime.now())
    except:
      print("Error recording PH")

"""
while True:
  data = ser.read()
  if(data == "\r"):
    print "Received from sensor:" + line
    line = ""
  else:
    line = line + data
"""

# The following will execute collect() if this isn't loaded by another module
if __name__ == '__main__':
  collect()
