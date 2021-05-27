from models import *
from config import *
from flask import render_template, jsonify, request


@app.route('/login', methods=['POST'])
def login():
    data=request.json
    curuser = db.session.query(User).filter(User.phone_number == data['phone_number']).first()
    if not curuser:
        return jsonify({"Error": "User not found"}), 404
    if not check_password_hash(curuser.password, data['password']):
        return jsonify({"Error": "Wrong password"}), 404
    return jsonify({'message': 'Success', 'id': curuser.id, 'role': curuser.role, 'username': curuser.email})

@app.route('/log_out', methods=['POST'])
def log_out():
    return jsonify({'message': 'Success'})