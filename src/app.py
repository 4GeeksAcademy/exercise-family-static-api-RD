"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#GET all family memebers
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

#GET one member by ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_fam_member(member_id):
    member =  jackson_family.get_member(member_id)
    return jsonify(member), 200

#POST add new member
@app.route('/members', methods=['POST'])
def add_fam_member():
    info = request.get_json()
    result = jackson_family.add_member(info)
    return jsonify(result), 200

#DELETE member by ID
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_fam_member(member_id):
    result = jackson_family.delete_member(member_id)
    return jsonify(result), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
