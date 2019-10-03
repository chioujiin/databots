import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from opencage.geocoder import OpenCageGeocode
#
# latitude1=0.0
# latitude2=0.0
# longitude1=0.0
# longitude2=0.0
def generate_coordinates(location1, location2):
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
    return(latitude1, longitude1, latitude2, longitude2)


latitude1, longitude1, latitude2, longitude2 = generate_coordinates("Toronto", "Houston")


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
    connection = mysql.connector.connect(host='52.14.83.188',
                                         database='yelp',
                                         user='databots',
                                         password='password')


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