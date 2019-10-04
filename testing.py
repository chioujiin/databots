from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response
import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
import logging
from opencage.geocoder import OpenCageGeocode
import json
import logging

app = Flask(__name__)
 
@app.route('/index')
@app.route('/')
def index():
  return render_template('search.html')
 
@app.route('/search', methods=['GET', 'POST'])
def getRestaurants():
    try:
        cursor = None

        city = request.args.get('city')
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
            row = cursor.fetchall()
            logging.warning("after fetchall")
            resp = []
            for result in row:
                resultDict = { 'a': result[0],
                'b': result[1],
                'c': result[2],
                'd': result[3],
                'e': result[4],
                'f': result[5],
                'g': result[6],
                'h': result[7],
                'i': result[8],
                'j': result[9],
                'k': result[10],
                'l': result[11],
                'm': result[12]
                }
                resp.append(resultDict)
            logging.warning("after for loop")
            logging.warning("before json dumps")
            return render_template('search.html', resp = json.dumps(resp))
            # return json.dumps(resp)
            # headers = {'Content-Type': 'text/html'}
            # return make_response(render_template('search.html', resp = json.dumps(resp)),200,headers)

        else:
            logging.warning("In else")
            return resp
    finally: print("end")
 
if __name__ == '__main__':
  app.run()