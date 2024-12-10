"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
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

@app.route('/user', methods=['GET'])
def get_all_users():
    try:

        users = User.query.all()
        if len(users) < 1:
            return jsonify({"msg": "not found"}), 404
        serialized_users = list(map(lambda x: x.serialize(), users))
        return jsonify(serialized_users), 200
    except Exception as e:
        return jsonify ({"msg": "Server error", "error": str(e)}), 500
    
@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"msg": f"user{user_id} not found"}), 404

        serialized_user = user.serialize()
        return jsonify(serialized_user), 200
    except Exception as e:
        return jsonify ({"msg": "Server error", "error": str(e)}), 500

# create user 
@app.route('/user', methods=['POST'])
def create_new_user():
    try:
        body= json.loads(request.data)
        new_user = User(
            email=body["email"],
            password=body["password"],
            is_active=True
        )
    
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User created", "user_id": new_user.id}), 201
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# get planets

@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets = Planet.query.all()
        if not planets:
            return jsonify({"msg": "No planets found"}), 404

        serialized_planets = [planet.serialize() for planet in planets]
        return jsonify(serialized_planets), 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"msg": f"Planet with ID {planet_id} not found"}), 404

        return jsonify(planet.serialize()), 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Get favorites

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    try:
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        if not favorites:
            return jsonify({"msg": f"No favorites found for user {user_id}"}), 404

        serialized_favorites = [favorite.serialize() for favorite in favorites]
        return jsonify(serialized_favorites), 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

    

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        body = request.json
        user_id = body.get("user_id")
        if not user_id:
            return jsonify({"msg": "User ID is required"}), 400

        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"msg": f"Planet with ID {planet_id} not found"}), 404

        new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"msg": f"Planet {planet_id} added to favorites for user {user_id}"}), 201
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

    
    
    
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        body = request.json
        user_id = body.get("user_id")  
        if not user_id:
            return jsonify({"msg": "User ID is required"}), 400

        favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if not favorite:
            return jsonify({"msg": f"Favorite planet with ID {planet_id} not found for user {user_id}"}), 404

        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": f"Planet {planet_id} removed from favorites for user {user_id}"}), 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500




@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    try:
        body = request.json
        user_id = body.get("user_id") 
        if not user_id:
            return jsonify({"msg": "User ID is required"}), 400

      
        person = People.query.get(people_id)
        if not person:
            return jsonify({"msg": f"Person with ID {people_id} not found"}), 404

  
        new_favorite = Favorite(user_id=user_id, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"msg": f"Person {people_id} added to favorites for user {user_id}"}), 201
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

    


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    try:
        body = request.json
        user_id = body.get("user_id") 
        if not user_id:
            return jsonify({"msg": "User ID is required"}), 400

        # Find the favorite
        favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
        if not favorite:
            return jsonify({"msg": f"Favorite person with ID {people_id} not found for user {user_id}"}), 404

        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": f"Person {people_id} removed from favorites for user {user_id}"}), 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

    





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)