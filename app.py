from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from models import ph
import datetime


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
  
  # The following mongo query will return the last 15 minutes worth of data points
  #  in list format
  ph_objs = ph.objects(time__gte=datetime.datetime.now() - datetime.timedelta(minutes=15)) 
  data = []
  time = []
  for i in ph_objs:
    data.append(i['ph'])
    time.append(i['time'].strftime("%I:%M%p"))

  # http://jsfiddle.net/gh/get/jquery/1.9.1/highslide-software/highcharts.com/tree/master/samples/highcharts/demo/line-basic/
  # Setup Chart
  chart = {"renderTo": 'chart', "type": 'line', "height": 350,}
  series = [{"name": 'pH', "data": data}]
  title = {"text": 'vFarm PH Levels'}
  xAxis = {"categories": time}
  yAxis = {"title": {"text": 'ph'}}

  return render_template('index.html',chartID='chart', chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

if __name__ == "__main__":
  app.run(debug=True,port=80,host="0.0.0.0")
