import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask import jsonify, request
import logging
import json
import datetime


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])


def getRestaurants():
    try:
        cursor = None

        city = request.args.get('city')
        preference=request.args.get('preference')
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
            return render_template('test.html', lenrow = len(row), lencol = len(row[0]), records1 = row)
        else:
            logging.warning("In else")
            return resp
    finally: print("end")
if __name__ == '__main__':
    app.run()
