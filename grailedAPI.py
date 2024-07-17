from flask import Flask,request
import priceEstimate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api,reqparse,fields,marshal_with,abort
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
app=Flask(__name__)
url=os.getenv("DATABASE_URL")
connection=psycopg2.connect(url)

CREATE_ITEM_TABLE=(
    'CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT, price INTEGER);'
)

INSERT_ITEM_RETURN_ID='INSERT INTO items (name,price) VALUES (%s,%s) RETURNING id;'

UPDATE_ITEM='UPDATE items SET price=%s WHERE name=%s;'

GET_ITEM='SELECT * FROM ITEMS WHERE name=%s;'

GET_ITEMS_IN_RANGE='SELECT * FROM ITEMS WHERE price BETWEEN %s AND %s;'

GET_ITEMS_WITH_KEYWORD='SELECT * FROM ITEMS WHERE name LIKE %s;'

@app.post('/api/items')
def create_item():
    data=request.get_json()
    name=data['name']
    price=priceEstimate.getAvgPrice(name)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ITEM_TABLE)
            cursor.execute(INSERT_ITEM_RETURN_ID,(name,price))
            item_id=cursor.fetchone()[0]
            cursor.close()
    return {'item_id':item_id,'message':f'Item {name} created'},201

@app.get('/api/items')
def get_item():
    data=request.get_json()
    name=data['name']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ITEM,(name,))
            price=cursor.fetchone()[2]
            cursor.close()
            return {'Item Name':name,'Price':'$'+str(price)}

@app.patch('/api/items')
def patch_item():
    data=request.get_json()
    name=data['name']
    price=priceEstimate.getAvgPrice(name,True)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ITEM_TABLE)
            cursor.execute(UPDATE_ITEM,(price,name))
            cursor.close()
    return {'message':f'Item {name} updated'},200
   

@app.get('/api/items/by-key')
def get_items_by_key():
    data=request.get_json()
    key='%'+data['key']+'%'
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ITEMS_WITH_KEYWORD,(key,))
            items=cursor.fetchall()
            cursor.close()
            return items

@app.get('/api/items/by-price')
def get_items_by_price():
    data=request.get_json()
    minPrice=data['minPrice']
    maxPrice=data['maxPrice']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ITEMS_IN_RANGE,(minPrice,maxPrice))
            items=cursor.fetchall()
            cursor.close()
            return items

@app.route('/')
def home():
    return '<h1>Flask REST</h1>' 

if __name__=='__main__':
    app.run(debug=True)