import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify, request, redirect, url_for
import logging
from opencage.geocoder import OpenCageGeocode
import simplejson as json
import datetime

app = Flask(__name__)

# when the search route is called by submitting the first button
@app.route('/search', methods=['GET', 'POST'])
def getRestaurants():
    try:
        cursor = None
        # we get the city and preference the user entered
        city = request.args.get('search')
        preference=request.args.get('Preference')
        # we get the date of that request to check if the stores are open that day
        today=datetime.datetime.now()
        day=today.strftime("%A").lower()
        if city:
            logging.warning("In if")
            # if the user enters a city, connect to the database
            conn = mysql.connector.connect(host='18.221.176.74',
                                           database='yelp',
                                           user='databots',
                                           password='Crazy@123')
            logging.warning("connection established")
            cursor = conn.cursor()
            logging.warning("cursor before select")
            logging.warning("city is")
            logging.warning(city)
            # query to get all the rows that suits the users input
            cursor.execute("SELECT a.name, a.address, a.city, a.stars, a.review_count, b."+day+" from business a, business_hours b where a.city = %s and a.categories like '%Restaurants%' and a.categories like concat('%',%s,'%') and a.business_id=b.business_id", (city,preference))
            logging.warning("select executed")
            # get all the data matching the query
            row = cursor.fetchall()
            logging.warning("after fetchall")
            resp = []
            # put the result in JSON format for rendering results in table
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
            temprow = json.dumps(row)
            # render the response to search.html, which is our result page 
            return render_template('search.html', lenrow = len(row), lencol = len(row[0]), records1 = row)
        else:
            logging.warning("In else")
            return resp
    finally: print("end")


# when the destination route is called by submitting the second button
@app.route('/destination', methods=['GET', 'POST'])
def searchRestaurants():
    try:
        cursor = None
        # we get the two cities and preference the user entered
        city1 = request.args.get('start')
        city2 = request.args.get('end')
        preference=request.args.get('Preference')
        # get the date and get the opening stores
        today = datetime.datetime.now()
        day = today.strftime("%A").lower()
        if (True):
            logging.warning("In if")
            # connect to the database
            conn = mysql.connector.connect(host='18.221.176.74',
                                           database='yelp',
                                           user='databots',
                                           password='Crazy@123')
            logging.warning("connection established")
            cursor = conn.cursor()
            logging.warning("cursor before select")
            logging.warning(city1)
            logging.warning(city2)

            # the function to get the coordinates for the two cities
            def generate_coordinates(city1, city2):
                logging.warning("inside geocode")
                key = "f89b26202bef4146a94c7d5c2f3a1648"
                geocoder = OpenCageGeocode(key)
                input1 = city1
                output1 = geocoder.geocode(input1)
                input2 = city2
                output2 = geocoder.geocode(input2)
                latitude1 = output1[0]['geometry']['lat']
                longitude1 = output1[0]['geometry']['lng']
                latitude2 = output2[0]['geometry']['lat']
                longitude2 = output2[0]['geometry']['lng']
                return (latitude1, longitude1, latitude2, longitude2)

            # get the coordinates for the two entered cities
            latitude1, longitude1, latitude2, longitude2 = generate_coordinates(city1,city2)

            # we want to get a regtangle whose four points are the four coordinates
            # and we want to return every restuarant with the entered preference within this regtangle
            # latitude_small is the latitude on the left and latitude_big is the latitude on the right
            # they compose the width of the regtangle
            if (latitude1 > latitude2):
                latitude_small = latitude2
                latitude_big = latitude1
            elif (latitude2 > latitude1):
                latitude_small = latitude1
                latitude_big = latitude2

            # longitude_small is the southern longitude and longitude_big is the northern longitude 
            # they compose the length of the regtangle
            if (longitude1 > longitude2):
                longitude_small = longitude2
                longitude_big = longitude1
            elif (longitude2 > longitude1):
                longitude_small = longitude1
                longitude_big = longitude2

            # we select all restaurant within the regtangle with the preference the user input
            cursor.execute("select a.name, a.address, a.city, a.stars, a.review_count, b."+day+" from business a, business_hours b where a.categories like '%Restaurants%' AND a.categories like concat('%',%s,'%') AND a.latitude between %s AND %s AND a.longitude between %s AND %s AND a.business_id=b.business_id",(preference, latitude_small, latitude_big, longitude_small, longitude_big))
            logging.warning("select executed")
            # get all the results
            row = cursor.fetchall()
            logging.warning("after fetchall")
            resp = []
            logging.warning("after for loop")
            logging.warning("before json dumps")
            temprow = json.dumps(row)

            # render the response to search.html, which is our result page 
            return render_template('./search.html', lenrow=len(row), lencol=len(row[0]), records1=row)
    finally:
        print("end")

# our index route
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()