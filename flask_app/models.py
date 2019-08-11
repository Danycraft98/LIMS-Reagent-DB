from flask_app import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	username = db.Column(db.String(255), nullable=False)
	password = db.Column(db.String(255), nullable=False)

class Manufacturer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	date_entered = db.Column(db.DateTime)
	part_num = db.Column(db.Integer)
	lot_num = db.Column(db.Integer)
	exp_date = db.Column(db.Integer)
	part_start = db.Column(db.Integer)
	part_end = db.Column(db.Integer)
	lot_start = db.Column(db.Integer)
	lot_end = db.Column(db.Integer)

	comp_barcode = db.Column(db.Integer)
	comp_part_num = db.Column(db.Integer)
	comp_lot_num = db.Column(db.Integer)
	comp_part_start = db.Column(db.Integer)
	comp_part_end = db.Column(db.Integer)
	comp_lot_start = db.Column(db.Integer)
	comp_lot_end = db.Column(db.Integer)
	kits = db.relationship('Kit', lazy=True)
	reagents = db.relationship('Reagent', lazy=True)


class Kit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	barcode = db.Column(db.String(255), nullable=False)
	part_num = db.Column(db.String(255))
	lot_num = db.Column(db.String(255))
	exp_date = db.Column(db.DateTime)
	date_entered = db.Column(db.DateTime)
	quantity = db.Column(db.Integer)
	manufacturer_fk = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)
	components = db.relationship('Component', lazy=True)


class Reagent(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	barcode = db.Column(db.String(255), nullable=False)
	part_num = db.Column(db.String(255))
	lot_num = db.Column(db.String(255))
	exp_date = db.Column(db.DateTime)
	date_entered = db.Column(db.DateTime)
	quantity = db.Column(db.Integer)
	manufacturer_fk = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)


class MadeReagent(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	exp_date = db.Column(db.DateTime)
	date_entered = db.Column(db.DateTime)
	quantity = db.Column(db.Integer)
	components = db.relationship('Component', lazy=True)


class Component(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	barcode = db.Column(db.String(255))
	part_num = db.Column(db.String(255))
	lot_num = db.Column(db.String(255))
	condition = db.Column(db.String(255), nullable=False)
	kit_fk = db.Column(db.Integer, db.ForeignKey('kit.id'))
	madereagent_fk = db.Column(db.Integer, db.ForeignKey('made_reagent.id'))