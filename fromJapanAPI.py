from flask import Flask,request
import priceEstimate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api,reqparse,fields,marshal_with,abort
import os
import psycopg2
from dotenv import load_dotenv
import scrapeFromJapan
from concurrent import futures

load_dotenv()
app=Flask(__name__)
url=os.getenv("DATABASE_URL")
connection=psycopg2.connect(url)

CREATE_FJPITEMS_TABLE=(
    '''CREATE TABLE IF NOT 
    EXISTS fjpItems (id SERIAL PRIMARY KEY, searchTerm TEXT, name TEXT, link TEXT, price INTEGER);'''
)

CREATE_IMAGES_TABLE=(
    '''CREATE TABLE IF NOT EXISTS images (id SERIAL PRIMARY KEY, itemID INTEGER, name TEXT, searchTerm TEXT, imageLink TEXT)'''
)

INSERT_ITEM_RETURN_ID='''INSERT INTO FJPITEMS (searchTerm,name,link,price) 
VALUES (%s,%s,%s,%s) RETURNING id;'''

GET_ITEM='SELECT * FROM FJPITEMS WHERE name=%s;'

GET_ITEMS_IN_RANGE='SELECT * FROM FJPITEMS WHERE price BETWEEN %s AND %s;'

GET_ITEMS_WITH_SEARCHTERM='SELECT * FROM FJPITEMS WHERE searchTerm=%s;'

GET_ITEMS_WITH_KEYWORD='SELECT * FROM FJPITEMS WHERE name LIKE %s;'

INSERT_IMAGES='INSERT INTO images (name,itemID,searchTerm,imageLink) VALUES (%s,%s,%s,%s)'

GET_IMAGES_BY_ITEM='SELECT * FROM images WHERE name=%s'

GET_IMAGES_BY_SEARCHTERM='SELECT * FROM images WHERE searchTerm=%s'

GET_IMAGES_BY_LIKETERMS='SELECT * FROM images WHERE searchTerm LIKE %s'

@app.post('/items/search')
def create_search():
    data=request.get_json()
    term=data['searchTerm']
    links=scrapeFromJapan.getTerm(term)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_FJPITEMS_TABLE)
            cursor.execute(CREATE_IMAGES_TABLE)
            with futures.ThreadPoolExecutor(max_workers=10) as executor:
                items=list(executor.map(scrapeFromJapan.getItem,links))
            for item in items:
                cursor.execute(INSERT_ITEM_RETURN_ID,(term,item['name'],item['link'],item['price']))
                item_id=cursor.fetchone()[0]
                for image in item['images']:
                    cursor.execute(INSERT_IMAGES,(item['name'],item_id,term,image))
            cursor.close()
            return {'message':f'Search for {term} executed successfully'},201

@app.post('/items')
def create_item():
    data=request.get_json()
    searchTerm=data['searchTerm']
    name=data['name']
    link=data['link']
    price=data['price']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_FJPITEMS_TABLE)
            cursor.execute(INSERT_ITEM_RETURN_ID,(searchTerm,name,link,price))
            item_id=cursor.fetchone()[0]
            cursor.close()
            return {'item_id':item_id,'message':f'Item {name} created'},201

@app.get('/items/by-term')
def get_items_by_term():
    data=request.get_json()
    term=data['searchTerm']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ITEMS_WITH_SEARCHTERM,(term,))
            items=cursor.fetchall()
            cursor.close()
            return items

@app.get('/items/by-like-term')
def get_items_by_like_term():
    data=request.get_json()
    term=data['searchTerm']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ITEMS_WITH_KEYWORD,(term,))
            items=cursor.fetchall()
            cursor.close()
            return items

@app.get('/items/by-price')
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
    app.run(debug=True, port=5001)