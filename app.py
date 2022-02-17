from flask import Flask, render_template, request, jsonify
import mysql.connector as mariadb
import mariadb
import json
from sensordata import captureData

app = Flask(__name__)

conn = mariadb.connect(
         host='localhost',
         user='sense',
         password='h@',
         database='sensedata',
         autocommit=True)

# Route to front page
@app.route("/", methods=['GET'])
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM measurement")
    rows = cur.fetchall()
    print(rows)
    return render_template("index.html", rows=rows)

# Route to see specific data by sensor id
@app.route("/sensor/<int:sensor_id>", methods=['GET'])
def get_sensor_data(sensor_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor")
    sensors = cur.fetchall()
    for uid in sensors:
        datatitle = uid[1]
        if uid[0] == sensor_id:
            cur.execute("SELECT * FROM measurement WHERE sensor_id=%s",[sensor_id])
            rows = cur.fetchall()
            ids = [i[0] for i in rows]
            labels = [x for x in ids]
            datapoints = [i[3] for i in rows]
            return render_template("sensor.html", sensor_id=sensor_id, rows=rows, labels=labels, datapoints=datapoints, datatitle=datatitle)

# Route to return all sensors in JSON
@app.route('/api/sensors', methods=['GET'])
def sensors_api():
   cur = conn.cursor()
   cur.execute("SELECT * FROM sensor")
   row_headers=[x[0] for x in cur.description]
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))
   return json.dumps(json_data)

# Route to return all measurements in JSON
@app.route('/api/measurements', methods=['GET'])
def measurements_api():
   cur = conn.cursor()
   cur.execute("SELECT * FROM measurement")
   row_headers=[x[0] for x in cur.description]
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))
   return json.dumps(json_data, default=str)

# Route to capture new measurements with a POST request and a button in HTML
# Calling function captureData() from sensordata.py
@app.route('/api/measurements/capture', methods=['GET', 'POST'])
def measurements_api_capture():
    captureData()
    return ('Data captured!<br /><br /><a href="/"><button>Front page</button></a>')

# Route to delete measurement
@app.route('/api/measurements/delete/<int:measurement_id>', methods=['GET', 'DELETE'])
def delete_measurement(measurement_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM measurement WHERE id=%s",[measurement_id])
    conn.commit()
    response = jsonify('Measurement deleted')
    response.status_code = 200
    return response

if __name__ == '__app__':
    app.run(host="0.0.0.0", debug=True, use_debugger=True, use_reloader=True)
