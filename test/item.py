from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import sqlite3
from flask_jwt import jwt_required
from db import db

from models.itemModel import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price"
            , type = float
            , required = True
            , help = "This field cannot be blank"
    )
    parser.add_argument("store_id"
            , type = int
            , required = True
            , help = "Every item needs a store id"
    )
    
    
    @jwt_required()
    def get(self, name):
        # data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        return (item.json(), 200) if item else ({"message" : "{} not found.".format(name)}, 404)
    
    @jwt_required()        
    def post(self, name):                      
        if ItemModel.find_by_name(name):
            return {"message" : "{} already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting {}.".format(name)}, 500

        return {"message" : "{} is added.".format(name)}, 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else: 
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()
        


    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "{} is deleted".format(name)}
        return {"message": "{} does not exist".format(name)}, 404


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = [item.json() for item in ItemModel.query.all()]
        return {"items": items}