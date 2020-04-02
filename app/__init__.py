from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from argparse import ArgumentParser
import os

# "Global" search bar variable
mySQL_con = 'mysql://root:@127.0.0.1/reagent_db'
host = '127.0.0.1:3307'
port = '3307'

# Setting up command line option interpreterc
parser = ArgumentParser()
parser.add_argument("-dbh", "--dbhost", type=str, metavar='', help="Add custom database host address")
parser.add_argument("-p", "--port", type=str, metavar='', help="Add custom database port")
args = parser.parse_args()

# App Setup
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': os.urandom(24),
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////Users/Daniel/PycharmProjects/Reagent-DB/app/database.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'UPLOAD_FOLDER': 'data'
})

# TODO: Database info here

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

from app import route, manufacturer_routes, kit_routes, reagent_routes, made_reagent_routes
