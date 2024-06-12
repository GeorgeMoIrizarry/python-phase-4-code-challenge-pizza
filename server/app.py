#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        all_restaurants = [] 
        for restaurant in Restaurant.query.all():
            all_restaurants.append(restaurant.to_dict(rules=('-restaurant_pizzas',)))
        return make_response(all_restaurants)
api.add_resource(Restaurants, '/restaurants')

class RestaurantById(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if restaurant:
            return make_response(restaurant.to_dict())
        else:
            return make_response({"error" : "Restaurant not found"}, 404)
    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response({"" : ""}, 204)
        else:
            return make_response({"error" : "Restaurant not found"}, 404)
class Pizzas(Resource):
    def get(self):
        all_pizzas = []
        for pizza in Pizza.query.all():
            all_pizzas.append(pizza.to_dict(rules=('-joined_relationship',)))
        return make_response(all_pizzas)
class MakeRestaurantPizza(Resource):
    def post(self):
        try:
            new_pizza = RestaurantPizza(
                price = request.json['price'],
                pizza_id = request.json['pizza_id'],
                restaurant_id = request.json['restaurant_id']
            )
            db.session.add(new_pizza)
            db.session.commit()
            return make_response(new_pizza.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
api.add_resource(MakeRestaurantPizza, '/restaurant_pizzas')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(RestaurantById, '/restaurants/<int:id>')



if __name__ == "__main__":
    app.run(port=5555, debug=True)
