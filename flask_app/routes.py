from flask import render_template, url_for, redirect, request
from flask_app import engine_RK, app



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
	return render_template('home.html')


@app.route("/reagents")
def reagents():
	return render_template('reagent.html', title='Reagent')


@app.route("/add_reagent", methods=['GET', 'POST'])
def reagent_add():
	return render_template('add_reagent.html', title='Add')


@app.route("/made-reagents")
def made_reagents():
	return render_template('made-reagent.html', title='Made Reagent')


@app.route("/add_made-reagent", methods=['GET', 'POST'])
def made_reagent_add():
	return render_template('add_made-reagent.html', title='Add')