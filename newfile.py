import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify, request, redirect, url_for
import logging
from opencage.geocoder import OpenCageGeocode
import simplejson as json

app = Flask(__name__)

@app.route('/search', methods=['GET', 'POST'])
def getRestaurants():
    try:
        cursor = None

        city = request.args.get("search")
        
        if city:
            logging.warning("In if")
            conn = mysql.connector.connect(host='18.221.176.74',
                                           database='yelp',
                                           user='databots',
                                           password='Crazy@123')
            logging.warning("connection established")
            cursor = conn.cursor()
            logging.warning("cursor before select")
            logging.warning("city is")
            logging.warning(city)
            cursor.execute("SELECT * from business where city = %s", (city,))
            logging.warning("select executed")
            row = cursor.fetchmany(3)
            # resp = jsonify(row)
            resp = row
            # resp.status_code = 200
            print(resp)
            return resp
        else:
            logging.warning("In else")
            resp = jsonify('User "city" not found in query string')
            # resp.status_code = 500
            return resp
    finally: 
        # if (conn.is_connected()):
        #     cursor.close()
        #     conn.close()
        #     print("MySQL connection is closed")
        print("here")
        print(resp)
        return render_template('search.html', data=json.dumps(resp))

#
# latitude1=0.0
# latitude2=0.0
# longitude1=0.0
# longitude2=0.0
@app.route('/destination', methods=['GET', 'POST'])
def generate_coordinates():
    location1 = request.args.get("start")
    location2 = request.args.get("end")
    key = "f89b26202bef4146a94c7d5c2f3a1648"
    geocoder = OpenCageGeocode(key)
    input1 = location1
    output1 = geocoder.geocode(input1)
    # print(output1)
    input2 = location2
    output2 = geocoder.geocode(input2)
    # print(output2)
    latitude1 = output1[0]['geometry']['lat']
    longitude1 = output1[0]['geometry']['lng']
    print(latitude1, longitude1)
    latitude2 = output2[0]['geometry']['lat']
    longitude2 = output2[0]['geometry']['lng']
    print(latitude2, longitude2)
    # return(latitude1, longitude1, latitude2, longitude2)


# latitude1, longitude1, latitude2, longitude2 = generate_coordinates("Toronto", "Houston")


    if(latitude1>latitude2):
        latitude_small = latitude2
        latitude_big = latitude1
    elif(latitude2>latitude1):
        latitude_small = latitude1
        latitude_big = latitude2


    if(longitude1>longitude2):
        longitude_small = longitude2
        longitude_big = longitude1
    elif(longitude2>longitude1):
        longitude_small = longitude1
        longitude_big = longitude2


    try:
        print("here in try")
        connection = mysql.connector.connect(host='18.221.176.74',
                                            database='yelp',
                                            user='databots',
                                            password='Crazy@123')


        #sqlselect_Query=("select name from business where latitude between %s AND %s AND longitude between %s AND %s",(latitude1,latitude2,longitide1,longitude2,))
        cursor = connection.cursor()
        print(latitude_small, longitude_small, latitude_big, longitude_big)

        sql_select_Query = """select name from business where latitude between %s AND %s AND longitude between %s AND %s"""

        cursor.execute(sql_select_Query,  (latitude_small, latitude_big, longitude_small, longitude_big))
        records = cursor.fetchall()
        print(records)
        print("Total number of rows in Laptop is: ", cursor.rowcount)

        print("\nPrinting each laptop record")

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

        return render_template('index.html', records = records)


    
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()