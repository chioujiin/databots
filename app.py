import pymongo
from flask import Flask, render_template, jsonify, request, redirect, url_for
from opencage.geocoder import OpenCageGeocode
import simplejson as json
import datetime
app = Flask(__name__)

# connect to mongoDB
client = pymongo.MongoClient("mongodb+srv://databots:Crazy123@databots-nmkwk.mongodb.net/test?retryWrites=true&w=majority")
db = client.yelp_new
collection = db.yelp_business

# when the user clicks the search button
@app.route('/search', methods=['GET', 'POST'])
def getRestaurants():
    try:
        # get the information the user entered
        city = request.args.get('search')
        stars = int(request.args.get('stars'))
        preference=request.args.get('Preference2')
        today=datetime.datetime.now()
        day=today.strftime("%A").lower()
        
        # if the user enters a city
        if city:
            # we get the documents that are as requested by the users
            result = collection.count_documents({"$and":[{'categories': {'$regex':preference}}, {'city':city}, {'stars' : {"$gte" : stars}}]})
            
            # if we didn't get anything, we use the build-in function from pymongo and return a 404 not found response to the front-end
            if result ==0: 
                result = collection.find_one_or_404({"$and":[{'categories': {'$regex':preference}}, {'city':city}, {'stars' : {"$gte" : stars}}]})
                return render_template('search.html', records = result)
            
            # if there are results, render the results on the search.html page
            else: 
                result = collection.find({"$and":[{'categories': {'$regex':preference}}, {'city':city}, {'stars' : {"$gt" : stars}}]})
                return render_template('search.html', records = result)
        else: return None
    finally:
        print('here')


# when the user clicks the find button
@app.route('/destination', methods=['GET', 'POST'])
def searchRestaurants():
    try:
        # get the information the user entered
        city1 = request.args.get('start')
        city2 = request.args.get('end')
        preference=request.args.get('Preference3')

        # get the date and get the opening stores
        today = datetime.datetime.now()
        day = today.strftime("%A").lower()

        # if the user enters both cities
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
            result = collection.find({"$and":[{'categories': {'$regex':preference}}, {'latitude' : { '$lt' : latitude_big ,"$gt" : latitude_small}}, {"longitude" : { "$lt" : longitude_big ,"$gt" : longitude_small}}, {'is_open': 1}]})
            # result = collection.find({"$and":[{  'categories': {'$regex':preference}}, {"longitude" : { "$lt" : longitude_big ,"$gt" : longitude_small}   }]})

            # render the response to search.html, which is our result page 
            return render_template('search.html', records = result)
    finally:
        print("done")

# when the user inserts data
@app.route('/insert', methods=['GET', 'POST'])
def insertDocument():
    try:
        # get the information the user entered
        stars = int(request.args.get('star'))
        restName = request.args.get('restName')
        city = request.args.get('city')
        state = request.args.get('state')
        categories = request.args.get('Preference1')

        # we assume the user will not enter the opening hours now
        # for implicit schema's sake, we have to set those to None so it will show correctly on the front-end
        doc = { "name":restName, "city": city,"state":state, "stars":stars,"categories": categories ,"monday":"None", "tuesday": "None", "wednesday": "None","thursday":"None", "friday": "None" ,"saturday":"None", "sunday": "None" }
        
        return render_template('index.html') 
    finally:
        print("done")

# the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()