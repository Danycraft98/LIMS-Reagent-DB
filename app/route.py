from flask import redirect, render_template, request, url_for
from flask import current_app as app
from flask_wtf import FlaskForm
from flask_login import login_user, login_required, logout_user, current_user

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import *


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4)])
    email = StringField('email')  # , validators=[InputRequired(), Email(message='invalid email')])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])


def search_query(items):
    filter_result = []
    item_types = [SuperKit, Kit, Reagent, MadeReagent]
    for item in items:
        for item_type in item_types:
            if hasattr(item_type, item) and items[item] != '':
                filter_result.extend(item_type.query.filter(getattr(item_type, item).like("%" + items[item] + "%")).all())
        if hasattr(Component, item) and items[item] != '':
            comps = Component.query.filter(getattr(Component, item).like("%" + items[item] + "%"))
            if comps.count() > 0:
                for comp in comps.all():
                    filter_result.extend(Kit.query.join(Component).filter(Component.id == comp.id))
                filter_result = list(set(filter_result))
    return filter_result


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        user = User.query.filter_by(username=form.get('username')).first()
        if user and check_password_hash(user.password, form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('home/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        hashed_pass = generate_password_hash(form.get('password'), method='sha256')
        new_user = User(name=form.get('name'), username=form.get('username'), email=form.get('email'), password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('home/register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('home/index.html', user=current_user.username)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        return render_template("home/elements.html", element_type='search_result', elements=search_query(request.form))
    return render_template('home/search.html', user=current_user.username)


@app.route("/<element_types>", methods=['GET', 'POST'])
@login_required
def elements(element_types):
    element_type = element_types[:-1]
    if element_type == 'manufacturer':
        element_list = Manufacturer.query.all()
    elif element_type == 'super_kit':
        element_list = SuperKit.query.all()
    elif element_type == 'kit':
        element_list = Kit.query.filter_by(super_kit_id=None).all()
    elif element_type == 'reagent':
        element_list = Reagent.query.all()
    elif element_type == 'made_reagent':
        element_list = MadeReagent.query.all()
    else:
        return page_not_found(None)
    return render_template("home/elements.html", element_type=element_type, elements=element_list)


@app.route("/delete_<element_type>/<int:element_id>")
@login_required
def delete(element_type, element_id):
    element = None
    if element_type == 'manufacturer':
        element = Manufacturer.query.get(element_id)
    if element_type == 'super_kit':
        element = SuperKit.query.get(element_id)
    elif element_type == 'kit':
        element = Kit.query.get(element_id)
    elif element_type == 'reagent':
        element = Reagent.query.get(element_id)
    elif element_type == 'made_reagent':
        element = MadeReagent.query.get(element_id)

    if element:
        db.session.delete(element)
        db.session.commit()
        return redirect(url_for('elements', element_types=element_type + 's'))
    else:
        return page_not_found(None)


def page_not_found(_):
    return render_template('404.html'), 404


app.register_error_handler(404, page_not_found)
