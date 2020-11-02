from argparse import ArgumentParser
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

# "Global" search bar variable
mySQL_con = 'mysql://root:@127.0.0.1/reagent_db'
host = '127.0.0.1:3307'
port = '3307'

# Setting up command line option interpreterc
parser = ArgumentParser()
parser.add_argument("-dbh", "--dbhost", type=str, metavar='', help="Add custom database host address")
parser.add_argument("-p", "--port", type=str, metavar='', help="Add custom database port")
args = parser.parse_args()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    bootstrap = Bootstrap(app)

    #app.config.from_object('config.Config')
    app.config.update(dict(
        SECRET_KEY="{{ LONG_RANDOM_STRING }}",
        # SQLALCHEMY_DATABASE_URI='mysql://irene:irene123@10.0.2.2/reagent_db',
        SQLALCHEMY_DATABASE_URI='mysql://root:password@localhost/reagent_db',
        # 'SQLALCHEMY_BINDS': {'reagent_db': mySQL_con},
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER='data'
    ))

    if args.dbhost:
        host = args.dbhost
        sqluser = os.environ['SQL_USER']
        sqlpass = os.environ['SQL_PASSWORD']
        if args.port:
            port = args.port
            mySQL_con = 'mysql://' + sqluser + ':' + sqlpass + '@' + host + ':' + port + '/reagent_db'
        else:
            mySQL_con = 'mysql://' + sqluser + ':' + sqlpass + '@' + host + '/reagent_db'

        app.config['SQLALCHEMY_BINDS'] = {'reagent_db': mySQL_con}

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    with app.app_context():
        from . import route, manufacturer_routes, kit_routes, reagent_routes, made_reagent_routes  # Import routes
        db.create_all()  # Create database tables for our data models

        return app
