import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template



try:
    connection = mysql.connector.connect(host='52.14.83.188',
                                         database='yelp',
                                         user='databots',
                                         password='password')

    sql_select_Query = "select * from business"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print("Total number of rows in Laptop is: ", cursor.rowcount)

    print("\nPrinting each laptop record")

except Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
