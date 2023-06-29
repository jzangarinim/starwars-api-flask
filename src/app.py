"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# /users ENDPOINTS
# GET ALL users
@app.route('/users', methods=['GET'])
def all_users():
    users = User()
    users = users.query.all()
    users = list(map(lambda item: item.serialize(), users))
    return jsonify(users), 200

# GET ONE user
@app.route('/users/<int:user_id>', methods=['GET'])
def handle_hello(user_id = None):
    user = User()
    if user_id is not None:
        user = user.query.get(user_id)
        if user is not None:
            return jsonify(user.serialize()), 200
        else:
            return jsonify({"message":"Not found"}), 404

# /users/favorites ENDPOINTS
# GET ALL favorites of ONE user
@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_user_favorites(id):
    favorites = Favorites()
    favorites = favorites.query.filter_by(user_id = id).all()
    favorites = list(map(lambda item: item.serialize(), favorites))
    try:
        return jsonify(favorites), 200
    except Exception as error:
        return jsonify({"message":"error"}), 400

# POST ONE favorite person/planet to ONE user
@app.route('/users/<int:u_id>/favorites/<nature>/<int:p_id>', methods=['POST'])
def add_favorite(nature, u_id = None,  p_id = None):
    if u_id is not None and p_id is not None:
        if nature == 'people':
            aux = Favorites()
            aux = aux.query.filter_by(user_id = u_id, people_id = p_id).first()
            if aux is None:
                favorite = Favorites(people_id = p_id, user_id = u_id)
                db.session.add(favorite)
                try:
                    db.session.commit()
                except Exception as error:
                    db.session.rollback()
                    return jsonify({"message":"error"}), 400
            else:
                return "Favorite character already exists in user's list", 200
        elif nature == 'planets':
            aux = Favorites()
            aux = aux.query.filter_by(user_id = u_id, planet_id = p_id).first()
            if aux is None:
                favorite = Favorites(planet_id = p_id, user_id = u_id)
                db.session.add(favorite)
                try:
                    db.session.commit()
                except Exception as error:
                    db.session.rollback()
                    return jsonify({"message":"error"}), 400
            else:
                return "Favorite already exists in user's list", 200
        else:
            return jsonify({"message":"Nature not recognized"}), 400
    return "Favorite added successfully!", 200

# DELETE ONE person/planet from ONE user's favorites list
@app.route('/users/<int:u_id>/favorites/<nature>/<int:p_id>', methods=['DELETE'])
def delete_favorite(nature, u_id = None,  p_id = None):
    if u_id is not None and p_id is not None:
        if nature == 'people':
            favorite = Favorites()
            favorite = favorite.query.filter_by(user_id = u_id, people_id = p_id).first()
            if favorite is not None:
                db.session.delete(favorite)
                try:
                    db.session.commit()
                except Exception as error:
                    db.session.rollback()
                    return jsonify({"message":"error"}), 400
            else:
                return "Character not found in user's favorites list", 200
        elif nature == 'planets':
            favorite = Favorites()
            favorite = favorite.query.filter_by(user_id = u_id, planet_id = p_id).first()
            if favorite is not None:
                db.session.delete(favorite)
                try:
                    db.session.commit()
                except Exception as error:
                    db.session.rollback()
                    return jsonify({"message":"error"}), 400
            else:
                return "Planet not found in user's favorites list", 200
        else:
            return jsonify({"message":"Nature not recognized"}), 400
    return "Favorite removed successfully!", 200

# /people endpoints
# GET ALL people
@app.route('/people', methods=['GET'])
def get_people():
    people = Character()
    people = people.query.all()
    people = list(map(lambda item: item.serialize(), people))
    return jsonify(people), 200

# POST ONE person
@app.route('/people', methods=['POST'])
def add_person():
    data = request.json
    aux = Character()
    aux = aux.query.filter_by(name=data["name"], eye_color=data["eye_color"], hair_color=data["hair_color"], height=data["height"], mass=data["mass"]).first()
    for key, value in data.items():
        if value is None or value == "":
            return f"Invalid/missing value in property: {key}", 400
    if aux is not None:
        return "Character already exists", 400
    else:
        people = Character()
        people = Character(name=data["name"], eye_color=data["eye_color"], hair_color=data["hair_color"], height=data["height"], mass=data["mass"])
        db.session.add(people)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return jsonify({"message":"error"}), 400
    return "Character added successfully!", 200

# GET ONE person
@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id = None):
    try:
        people = Character()
        people = people.query.get(person_id)
        return jsonify(people.serialize()), 200
    except Exception as error:
        return jsonify({"message":"Character not found"}), 404

# /planets endpoints
# GET ALL planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planet = Planet()
    planet = planet.query.all()
    planet = list(map(lambda item: item.serialize(), planet))
    return jsonify(planet), 200

# POST ONE planet
@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.json
    print(data)
    aux = Planet()
    aux = aux.query.filter_by(name=data["name"], climate=data["climate"], terrain=data["terrain"], population=data["population"]).first()
    for key, value in data.items():
        if value is None or value == "":
            return f"Invalid/missing value in property: {key}", 400
    if aux is not None:
        return "Planet already exists", 400
    else:
        planet = Planet()
        planet = Planet(name=data["name"], climate=data["climate"], terrain=data["terrain"], population=data["population"])
        db.session.add(planet)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return jsonify({"message":"error"}), 400
    return "Planet added successfully!", 200

# GET ONE planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id = None):
    try:
        planet = Planet()
        planet = planet.query.get(planet_id)
        return jsonify(planet.serialize()), 200
    except Exception as error:
        return jsonify({"message":"Planet not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
