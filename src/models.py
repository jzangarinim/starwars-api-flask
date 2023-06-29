from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(20), nullable=False)
    hair_color = db.Column(db.String(20), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    favorites = db.relationship('Favorites', backref='character', lazy=True)
    
    def __repr__(self):
        return f"<Character {self.name}>"

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "eye_color":self.eye_color,
            "hair_color":self.hair_color,
            "height":self.height,
            "mass":self.mass
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    favorites = db.relationship('Favorites', backref='planet', lazy=True)

    def __repr__(self):
        return f"<Planet {self.name}>"

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "climate":self.climate,
            "terrain":self.terrain,
            "population":self.population
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Favorite {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }

""" class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        } """