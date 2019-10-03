from flask import render_template, redirect, request, flash, url_for
from flask_app import app, db, current_user
from flask_app.models import User


@app.route("/", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = User.query.filter_by(username=request.form.get('username'),password=request.form.get('password')).first()
		if user:
			current_user.set_user(user)
			return redirect('home')
		else:
			flash("Wrong username or password")
	return render_template('login.html', before_home=True)


@app.route("/logout")
def logout():
	current_user.set_user(None)
	return redirect(url_for('login'))


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
	return render_template('register.html', before_home=True)


@app.route("/home")
def home():
	if not current_user.logged_in():
		return redirect(url_for('login'))
	return render_template('home.html')