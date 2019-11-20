import pymongo
from flask import Flask, render_template, jsonify, request, redirect, url_for
from opencage.geocoder import OpenCageGeocode
import simplejson as json
import datetime

app = Flask(__name__)


client = pymongo.MongoClient("mongodb+srv://databots:Crazy123@databots-nmkwk.mongodb.net/test?retryWrites=true&w=majority")
db = client.yelp_new
collection = db.yelp_business

@app.route('/search', methods=['GET', 'POST'])
def getRestaurants():
    try:
        city = request.args.get('search')
        preference=request.args.get('Preference')
        today=datetime.datetime.now()
        day=today.strftime("%A").lower()
        if city:
            result = collection.find({"$and":[{'categories': {'$regex':preference}}, {'city':city}]})

            return render_template('search.html', records = result)
        else:
            return None
    finally:
        print('here')



@app.route('/destination', methods=['GET', 'POST'])
def searchRestaurants():
    try:
        city1 = request.args.get('start')
        city2 = request.args.get('end')
        preference=request.args.get('Preference')
        # get the date and get the opening stores
        today = datetime.datetime.now()
        day = today.strftime("%A").lower()
        if (city1 and city2):

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
            result = collection.find({"$and":[{'categories': {'$regex':preference}}, {'latitude' : { '$lt' : latitude_big ,"$gt" : latitude_small}}, {"longitude" : { "$lt" : longitude_big ,"$gt" : longitude_small}}]})
            # result = collection.find({"$and":[{  'categories': {'$regex':preference}}, {"longitude" : { "$lt" : longitude_big ,"$gt" : longitude_small}   }]})

            # render the response to search.html, which is our result page 
            return render_template('search.html', records = result)
    finally:
        print("done")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()