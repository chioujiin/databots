from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{databots}:{password}@{52.14.83.188:3306}/{yelp}'
db = SQLAlchemy(app)

result = db.engine.execute(" SELECT top 10 from business;")
print (result)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 80)


