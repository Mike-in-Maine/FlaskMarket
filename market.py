from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import xmltodict, json
import untangle
import pymysql
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://miky1973:itff2020@mysql.irish-booksellers.com:3306/irishbooksellers'
db = SQLAlchemy(app)


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///market.db'
#db = SQLAlchemy(app)

app.config['SECRET_KEY'] = ""

def get_db_connection():
    #conn = sqlite3.connect('market.db')
    conn = sqlalchemy.create_engine('mysql+pymysql://miky1973:itff2020@mysql.irish-booksellers.com:3306/irishbooksellers')
    return conn

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable = False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable = False, unique = True)

    def __repr__(self):
        return f'Item {self.Item}'


@app.route('/')
def home_page():
    #conn = get_db_connection()
    #prices = conn.execute('SELECT * FROM orders ORDER BY 1').fetchall()
    #print(prices)
    #conn.close()

    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/market')
def market_page():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM orders ORDER BY ORDERDATE DESC LIMIT 300').fetchall()
    #df = pd.DataFrame(items)
    #df.sort_values(by=[1], inplace=True, ascending = True)
    return render_template('market.html', items = items)

def get_abe_API_neworders():
    df = pd.DataFrame()
    data = """
    <?xml version="1.0" encoding="ISO-8859-1"?>
    <orderUpdateRequest version="1.1">
        <action name="getAllNewOrders">
            <username>irishbooksellers</username>
            <password>ef624a8bd5a843cda651</password>
        </action>
    </orderUpdateRequest>
    """
    headers = {'username': 'irishbooksellers','password': 'ef624a8bd5a843cda651'}
    response = requests.get('https://orderupdate.abebooks.com:10003', data=data, headers=headers)
    print(response.text)
    root = ET.fromstring(response.text)
    dump = xmltodict.parse(response.text)

    obj = untangle.parse(response.text)
    emails = []
    citys = []
    codes = []
    countrys = []
    names = []
    phones = []
    regions = []
    streets = []
    street2s = []


    for po in root.findall('purchaseOrderList'):
        for po2 in po.findall('purchaseOrder'):
            for po3 in po2.findall('buyer'):
                for po4 in po3.findall('mailingAddress'):
                    city = po4.find('city').text
                    code = po4.find('code').text
                    country = po4.find('country').text
                    name = po4.find('name').text
                    phone = po4.find('phone').text
                    region = po4.find('region').text
                    street = po4.find('street').text
                    street2 = po4.find('street2').text
                    citys.append(city)
                    codes.append(code)
                    countrys.append(country)
                    names.append(name)
                    phones.append(phone)
                    regions.append(region)
                    streets.append(street)
                    street2s.append(street2)
    print(citys)
    print(codes)
    print(countrys)
    print(phones)
    print(names)
    print(phones)
    print(regions)
    print(streets)
    print(street2s)

    print(len(citys))
    print(len(codes))
    print(len(countrys))
    print(len(names))
    print(len(phones))
    print(len(regions))
    print(len(streets))
    print(len(street2s))

    yield citys


#sql connection to dreamhost
engine = sqlalchemy.create_engine('mysql+pymysql://miky1973:itff2020@mysql.irish-booksellers.com:3306/irishbooksellers')


if __name__ == '__main__':
    app.run(debug=True)

