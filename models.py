from mongoengine import connect, Document, DateTimeField, FloatField, BooleanField
import datetime

db = connect('vfarm', host='192.168.1.133', port=27017)

class ph(Document):
  time = DateTimeField(default=datetime.datetime.now())
  ph = FloatField()

class temperature(Document):
  time = DateTimeField(default=datetime.datetime.now())
  temp = FloatField()
