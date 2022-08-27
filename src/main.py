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
from models import People, Planets, db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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

@app.route('/people', methods=['GET'])
@app.route('/people/<int:user_id>', methods=['GET'])
def people_id(user_id = None):
    if request.method == 'GET':
        if user_id is None:
            people = People()
            people = people.query.all()
            
            return jsonify(list(map(lambda item: item.serialize(), people))) , 200
        else:
            people = People()
            people = people.query.get(user_id)
            if people:
                return jsonify(people.serialize())
            
        return jsonify({"message":"not found"}), 404



@app.route('/planets', methods=['GET'])
@app.route('/planets/<int:user_id>', methods=['GET'])
def planets_id(user_id = None):
    if request.method == 'GET':
        if user_id is None:
            planets = Planets()
            planets = planets.query.all()
            
            return jsonify(list(map(lambda item: item.serialize(), planets))) , 200
        else:
            planets = Planets()
            planets = planets.query.get(user_id)
            if planets:
                return jsonify(planets.serialize())
            
        return jsonify({"message":"not found"}), 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
