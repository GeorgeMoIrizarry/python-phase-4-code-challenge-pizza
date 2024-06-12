from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.Relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')
    pizzas = association_proxy('restaurant_pizzas', 'pizza')
    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant',)
    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    joined_relationship = db.Relationship('RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan')
    restaurants = association_proxy('joined_relationship', 'restaurant')
    # add serialization rules
    serialize_rules = ('-joined_relationship.pizza',)
    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    # add relationships
    pizza = db.Relationship('Pizza', back_populates='joined_relationship')
    restaurant = db.Relationship('Restaurant', back_populates='restaurant_pizzas')
    # add serialization rules
    serialize_rules = ('-pizza.joined_relationship', '-restaurant.restaurant_pizzas')
    # add validation
    @validates('price')
    def set_price(self, key, price):
        if 1 <= price <= 30:
            return price 
        else: 
            raise ValueError("Price value must be between 1 and 30")
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
