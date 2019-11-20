import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify, request, redirect, url_for
from opencage.geocoder import OpenCageGeocode
import simplejson as json
import datetime

app = Flask(__name__)

# when the search route is called by submitting the first button
@app.route('/search', methods=['GET', 'POST'])
def getRestaurants():
    try:
        # we get the city and preference the user entered
        city = request.args.get('search')
        preference=request.args.get('Preference')
        # we get the date of that request to check if the stores are open that day 
        today=datetime.datetime.now()
        day=today.strftime("%A").lower()
        if city:
            # if the user enters a city, connect to the database
            conn = mysql.connector.connect(host='18.221.176.74',
                                           database='yelp',
                                           user='databots',
                                           password='Crazy@123')
            cursor = conn.cursor()
            # query to get all the rows that suits the users input
            # get all the data matching the query
            cursor.execute("SELECT a.name, a.address, a.city, a.stars, a.review_count, b."+day+" from business a, business_hours b where a.city = %s and a.categories like '%Restaurants%' and a.categories like concat('%',%s,'%') and a.business_id=b.business_id", (city,preference))
            resultSet = cursor.fetchall()
            # render the response to search.html, which is our result page 
            return render_template('search.html', lenrow = len(resultSet), lencol = len(resultSet[0]), records = resultSet)
        else:
            return resultSet
    finally:
        if(conn):
            conn.close()

# when the destination route is called by submitting the second button
@app.route('/destination', methods=['GET', 'POST'])
def searchRestaurants():
    try:
        # we get the two cities and preference the user entered
        city1 = request.args.get('start')
        city2 = request.args.get('end')
        preference=request.args.get('Preference')
        # get the date and get the opening stores
        today = datetime.datetime.now()
        day = today.strftime("%A").lower()
        if (city1 and city2):
            # connect to the database
            conn = mysql.connector.connect(host='18.221.176.74',
                                           database='yelp',
                                           user='databots',
                                           password='Crazy@123')
            cursor = conn.cursor()

            # the function to get the coordinates for the two cities
            def generate_coordinates(city1, city2):
                key = "f89b26202bef4146a94c7d5c2f3a1648"
                geocoder = OpenCageGeocode(key)
                city1coordinates = geocoder.geocode(city1)
                city2coordinates = geocoder.geocode(city2)
                latitude1 = city1coordinates[0]['geometry']['lat']
                longitude1 = city1coordinates[0]['geometry']['lng']
                latitude2 = city2coordinates[0]['geometry']['lat']
                longitude2 = city2coordinates[0]['geometry']['lng']
                return (latitude1, longitude1, latitude2, longitude2)

            # get the coordinates for the two entered cities
            latitude1, longitude1, latitude2, longitude2 = generate_coordinates(city1,city2)

            # we want to get a rectangle whose four points are the four coordinates
            # and we want to return every restuarant with the entered preference within this rectangle
            # latitude_small is the latitude on the left and latitude_big is the latitude on the right
            # they compose the width of the rectangle
            if (latitude1 > latitude2):
                latitude_small = latitude2
                latitude_big = latitude1
            elif (latitude2 > latitude1):
                latitude_small = latitude1
                latitude_big = latitude2

            # longitude_small is the southern longitude and longitude_big is the northern longitude 
            # they compose the length of the rectangle
            if (longitude1 > longitude2):
                longitude_small = longitude2
                longitude_big = longitude1
            elif (longitude2 > longitude1):
                longitude_small = longitude1
                longitude_big = longitude2

            # we select all restaurant within the regtangle with the preference the user input
            cursor.execute("select a.name, a.address, a.city, a.stars, a.review_count, b."+day+" from business a, business_hours b where a.categories like '%Restaurants%' AND a.categories like concat('%',%s,'%') AND a.latitude between %s AND %s AND a.longitude between %s AND %s AND a.business_id=b.business_id",(preference, latitude_small, latitude_big, longitude_small, longitude_big))
            resultSet = cursor.fetchall()

            # render the response to search.html, which is our result page 
            return render_template('./search.html', lenrow=len(resultSet), lencol=len(resultSet[0]), records=resultSet)
        else:
            return resultSet
    finally:
        if(conn):
            conn.close()
    
# our index route
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()