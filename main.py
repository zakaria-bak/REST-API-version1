from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app =  Flask(__name__)
app.secret_key = "uefefo"
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

#liste to store items
items = []

class Item(Resource):
    # creating a parser
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help = "this field cannot left blank")


    # creating a get & post methods
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x : x['name'] == name, items), None)
        return {"item" : item}

    def post(self, name):
        #check the item exist
        if next(filter(lambda x : x['name'] == name, items), None):
            return {'message' : "An item with name {} already exist".format(name)}
                
        data = Item.parser.parse_args()
        item = {"name" : name, "price" : data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x : x['name'] != name, items))
        return {'message' : "item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x : x['name'] == name, items), None)
        if item is None: # if item doesnt exist we create it
            item = {"name" : name, "price" : data['price']}
            items.append(item)
        else:
            item.update(data) 

        return item


class Itemlist(Resource):
    def get(self):
        return {"items" : items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Itemlist, '/items')

if __name__ == "__main__":
    app.run(debug=True)