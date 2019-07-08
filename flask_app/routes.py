from flask import render_template, redirect, request, flash
from flask_app import app, db
from flask_app.models import User


@app.route("/", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = User.query.filter_by(username=request.form.get('username'),password=request.form.get('password')).first()
		if user:
			return redirect('home')
	return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		user = User.query.filter_by(username=username).first()
		if not user:
			if password == request.form.get('password2'):
				user = User(
					name=request.form.get('name'),
					username=username,
					password=password
				)
				db.session.add(user)
				db.session.commit()
				return redirect('home')
			else:
				flash("Password is not matched")
		else:
			flash("Username already exist")
	return render_template('register.html')


@app.route("/home")
def home():
	return render_template('home.html')