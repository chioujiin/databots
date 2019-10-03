from flask import Flask, render_template, jsonify, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
import logging
from opencage.geocoder import OpenCageGeocode

app = Flask(__name__)
 
@app.route('/index')
@app.route('/')
def index():
  return render_template('index.html')
 
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
        return render_template('search.html', data=jsonify(resp))
 
 
if __name__ == '__main__':
  app.run()