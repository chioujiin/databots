import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify, request, redirect, url_for
import logging
from opencage.geocoder import OpenCageGeocode
import simplejson as json
import datetime

app = Flask(__name__)

@app.route('/search', methods=['GET', 'POST'])
def getRestaurants():
    try:
        cursor = None

        city = request.args.get('search')
        preference=request.args.get('Preference')
        print("preference", preference, "city", city)
        today=datetime.datetime.now()
        day=today.strftime("%A").lower()
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
            cursor.execute("SELECT a.name, a.address, a.city, a.stars, a.review_count, b."+day+" from business a, business_hours b where a.city = %s and a.categories like '%Restaurants%' and a.categories like concat('%',%s,'%') and a.business_id=b.business_id", (city,preference))
            # cursor.execute("SELECT a.name, a.address, a.city, a.stars, a.review_count, b."+day+" from business a, business_hours b where a.city = %s  and a.business_id=b.business_id", (city,))

            logging.warning("select executed")
            row = cursor.fetchall()
            logging.warning("after fetchall")
            resp = []
            for result in row:
                resultDict = { 'name': result[0],
                'address': result[1],
                'city': result[2],
                'stars': result[3],
                'review count': result[4]
    
                }
                resp.append(resultDict)
            logging.warning("after for loop")
            logging.warning("before json dumps")
            #print(resp[0])
            #print(type(resp[0]))
            temprow = json.dumps(row)
            print(temprow)
            print("type of temprow", type(temprow))
            #print(jsonify.resp[0])
            #print(json.dumps(resp[0]))
            #temp = json.dumps(resp)
            #print(temp)
            print("type of row", type(row))
            #return jsonify(row)
            return render_template('search.html', lenrow = len(row), lencol = len(row[0]), records1 = row)
        else:
            logging.warning("In else")
            return resp
    finally: print("end")



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