from flask import Flask, request, jsonify, session as cursession
from flask_sqlalchemy import SQLAlchemy
import os
from flask_httpauth import HTTPBasicAuth
from sqlalchemy_utils import database_exists, create_database
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS

auth = HTTPBasicAuth()

app = Flask(__name__)
CORS(app, support_credentials=True)
app.secret_key = 'secret secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = URL = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root',
    password='root',
    server='localhost',
    database='audience_reservation_db'
)

if not database_exists(URL):
    create_database(URL)
db = SQLAlchemy(app)
engine = db.engine
Base = db.Model