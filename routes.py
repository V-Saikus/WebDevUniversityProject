from models import *
from config import *
from flask import render_template, jsonify, request


@app.route('/sign_up')
def sign_up_page():
    return render_template('sign_up.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/audiences')
def audiences_page():
    return render_template('audiences.html')

@app.route('/')
def homepage():
    return render_template('audiences.html')


@app.route('/login', methods=['POST'])
def login():
    curuser = db.session.query(User).filter(User.phone_number == request.form['phone_number']).first()
    if not curuser:
        return jsonify({"Error": "User not found"}), 404
    if not check_password_hash(curuser.password, request.form['password']):
        return jsonify({"Error": "Wrong password"}), 404
    cursession['username'] = curuser.email
    cursession['password'] = request.form['password']
    cursession['id'] = curuser.id
    return jsonify({"Success": "User logined"}), 200


@app.route('/log_out', methods=['POST'])
def log_out():
    cursession['username'] = None
    cursession['password'] = None
    cursession['id'] = None
    return jsonify({'Success': 'Logout success'})