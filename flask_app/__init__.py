from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from argparse import ArgumentParser
from sqlalchemy import create_engine
import os


class CurrentUser:
	user = None

	def set_user(self, user):
		self.user = user

	def logged_in(self):
		return self.user is not None


# "Global" search bar variable
search_in = ''
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
	'SQLALCHEMY_DATABASE_URI':'sqlite:///site.db'
})
"""'OIDC_CLIENT_SECRETS': 'client_secrets.json',
	'OIDC_VALID_ISSUERS': ['http://localhost:8080/auth/realms/RK_LIMS'],
	'OVERWRITE_REDIRECT_URI': 'http://localhost:5000/main',
	'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
	'OIDC_TOKEN_TYPE_HINT': 'access_token',
	'OIDC_OPENID_REALM': 'RK_LIMS',
	'TESTING': True,
	'DEBUG': True
})

if args.dbhost:
	host = args.dbhost
	sqluser = os.environ['SQL_USER']
	sqlpass = os.environ['SQL_PASSWORD']
	if args.port:
		port = args.port
		mySQL_con = 'mysql://' + sqluser + ':' + sqlpass + '@' + host + ':' + port + '/RK_LIMS'
	else:
		mySQL_con = 'mysql://' + sqluser + ':' + sqlpass + '@' + host + '/RK_LIMS'
"""
app.config['SQLALCHEMY_BINDS'] = {'RK_LIMS': mySQL_con}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


engine_RK = create_engine(mySQL_con)
db = SQLAlchemy(app)


from flask_app import routes, kit_routes, manufacturer_routes, reagent_routes, made_reagent_routes
