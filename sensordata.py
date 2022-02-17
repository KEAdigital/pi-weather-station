from sense_hat import SenseHat
import time
import mysql.connector as mariadb

def captureData():
    sensor_temp = 'Temperature'
    sensor_hum = 'Humidity'
    sensor_pres = 'Pressure'

    dbconfig = {
    'user': 'sensemeasure',
    'password': 'h@',
    'host': 'localhost',
    'database': 'sensedata',
    }

    sh = SenseHat()

    mariadb_connection = mariadb.connect(**dbconfig)

    cursor = mariadb_connection.cursor()

    cursor.execute("SELECT id FROM sensor WHERE name=%s",[sensor_temp])
    sensor_temp_id = cursor.fetchone()
    cursor.execute("SELECT id FROM sensor WHERE name=%s",[sensor_hum])
    sensor_hum_id = cursor.fetchone()
    cursor.execute("SELECT id FROM sensor WHERE name=%s",[sensor_pres])
    sensor_pres_id = cursor.fetchone()

    # Take readings from all three sensors
    t = round(sh.get_temperature(), 1)
    h = round(sh.get_humidity(), 1)
    p = round(sh.get_pressure(), 1)

    # Round the values to one decimal place
    t = round(t, 1)
    h = round(h, 1)
    p = round(p, 1)

    # Measure offset
    tempOffset = 10
    presOffset = 20
    humOffset = 1

    temp = t - tempOffset
    pres = p - presOffset
    hum = h - humOffset

    temp = round(temp, 1)
    pres = round(pres, 1)
    hum = round(hum, 1)

    # print("Raw temperature: %s C" % t)
    # print("Calculated temperature: %s Celsius" % temp + " | With offset: %s C" % tempOffset)
    # print("Raw pressure: %s MB" % p)
    # print("Calculated temperature: %s Milibar" % pres + " | With offset: %s C" % presOffset)
    # print("Raw humidity: %s Percentage" % h)
    # print("Calculated temperature: %s Percentage" % hum + " | With offset: %s C" % humOffset)

    cursor.execute('INSERT INTO measurement (value, sensor_id) VALUES (%s, %s);', (temp, sensor_temp_id[0]))
    cursor.execute('INSERT INTO measurement (value, sensor_id) VALUES (%s, %s);', (pres, sensor_pres_id[0]))
    cursor.execute('INSERT INTO measurement (value, sensor_id) VALUES (%s, %s);', (hum, sensor_hum_id[0]))
    mariadb_connection.commit()

    cur = mariadb_connection.cursor()
    cur.execute("SELECT * FROM measurement")
    rows = cur.fetchall()
    print(rows)

    # print("Data saved in database.")
    mariadb_connection.close()
