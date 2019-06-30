from flask import render_template, url_for, redirect, request
from flask_app import engine_RK, app



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
	return render_template('home.html')