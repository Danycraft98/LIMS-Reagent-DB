from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from argparse import ArgumentParser
import os


class CurrentUser:
    user = None

    def set_user(self, user):
        self.user = user

    def get_name(self):
        return self.user.name

    def logged_in(self):
        return self.user is not None


# "Global" search bar variable
mySQL_con = 'mysql://root:@127.0.0.1/reagent_db'
host = '127.0.0.1:3307'
port = '3307'

# Setting up command line option interpreter
parser = ArgumentParser()
parser.add_argument("-dbh", "--dbhost", type=str, metavar='', help="Add custom database host address")
parser.add_argument("-p", "--port", type=str, metavar='', help="Add custom database port")
args = parser.parse_args()

# App Setup
app = Flask(__name__)
current_user = CurrentUser()
app.config.update({
    'SECRET_KEY': os.urandom(24),
    # 'SQLALCHEMY_DATABASE_URI':'mysql://irene:irene123@10.0.2.2/reagent_db'
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///site.db'
    # 'SQLALCHEMY_DATABASE_URI':'mysql://root:@localhost/reagent_db'
})

"""
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
"""
db = SQLAlchemy(app)

from flask_app import routes, kit_routes, manufacturer_routes, reagent_routes, made_reagent_routes
