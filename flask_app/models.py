from flask_app import db


class Manufacturer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	kit_part_num = db.Column(db.Integer)
	kit_lot_num = db.Column(db.Integer)
	exp_date = db.Column(db.Integer)
	kit_part_start = db.Column(db.Integer)
	kit_part_end = db.Column(db.Integer)
	kit_lot_start = db.Column(db.Integer)
	kit_lot_end = db.Column(db.Integer)

	comp_barcode = db.Column(db.Integer)
	part_num = db.Column(db.Integer)
	lot_num = db.Column(db.Integer)
	part_start = db.Column(db.Integer)
	part_end = db.Column(db.Integer)
	lot_start = db.Column(db.Integer)
	lot_end = db.Column(db.Integer)
	kits = db.relationship('Kit', lazy=True)


class Kit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	barcode = db.Column(db.String(255), nullable=False)
	part_num = db.Column(db.Integer)
	lot_num = db.Column(db.Integer)
	exp_date = db.Column(db.DateTime)
	quantity = db.Column(db.Integer)
	manufacturer_fk = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)
	components = db.relationship('Component', lazy=True)


class Component(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	barcode = db.Column(db.Integer)
	part_num = db.Column(db.Integer)
	lot_num = db.Column(db.Integer)
	condition = db.Column(db.String(255), nullable=False)
	kit_fk = db.Column(db.Integer, db.ForeignKey('kit.id'), nullable=False)