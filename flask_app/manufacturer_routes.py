from flask import render_template, url_for, redirect, request
from flask_app import app, db, current_user
from flask_app.models import Manufacturer
from datetime import datetime


@app.route("/manufacturers", methods=['GET', 'POST'])
def manufacturers():
	if not current_user.logged_in():
		return redirect(url_for('login'))
	all_manufacturers = Manufacturer.query.all()
	if request.method == 'POST':
		return render_template("manufacturer/manufacturers.html", manufacturers=Manufacturer.query.filter_by(name=request.form.get('searchbox')), all_manufacturers=all_manufacturers)
	return render_template("manufacturer/manufacturers.html", manufacturers=all_manufacturers, all_manufacturers=all_manufacturers)


@app.route("/manufacturer/<int:manufacturer_id>")
def manufacturer(manufacturer_id):
	if not current_user.logged_in():
		return redirect(url_for('login'))
	manufacturer = Manufacturer.query.get(manufacturer_id)
	return render_template("manufacturer/manufacturer.html", manufacturer=manufacturer)


@app.route("/add_manufacturer", methods=["GET", "POST"])
def add_manufacturer():
	if not current_user.logged_in():
		return redirect(url_for('login'))
	return render_template("manufacturer/add_manufacturer.html")


@app.route("/add_manufacturer_redirect", methods=["GET", "POST"])
def add_manufacturer_redirect():
	# Request values from html inputs
	cb = {"part_num":0, "lot_num":0, "exp_date": 0}
	for item in request.form.getlist("cb"):
		cb[item] = 1

	try:
		part_start = int(request.form.get("part_start"))
		part_end = len(request.form.get("part_num")) + part_start
	except:
		part_start = part_end = -1

	try:
		lot_start = int(request.form.get("lot_start"))
		lot_end = len(request.form.get("lot_num")) + lot_start
	except:
		lot_start = lot_end = -1

	comp_cb = {"barcode":0,"part_num": 0, "lot_num": 0}
	for item in request.form.getlist("comp_cb"):
		comp_cb[item] = 1

	try:
		comp_part_start = int(request.form.get("comp_part_start"))
		comp_part_end = len(request.form.get("comp_part_num")) + comp_part_start
	except:
		comp_part_start = comp_part_end = -1

	try:
		comp_lot_start = int(request.form.get("comp_lot_start"))
		comp_lot_end = len(request.form.get("comp_lot_num")) + comp_lot_start
	except:
		comp_lot_start = comp_lot_end = -1

	manufacturer = Manufacturer(
		name = request.form.get("manu_name"),
		date_entered=datetime.today(),
		exp_date = cb["exp_date"],
		part_num = cb["part_num"],
		lot_num = cb["lot_num"],
		part_start = part_start,
		part_end = part_end,
		lot_start = lot_start,
		lot_end = lot_end,
		comp_barcode = comp_cb["barcode"],
		comp_part_num = comp_cb["part_num"],
		comp_lot_num = comp_cb["lot_num"],
		comp_part_start = comp_part_start,
		comp_part_end = comp_part_end,
		comp_lot_start = comp_lot_start,
		comp_lot_end = comp_lot_end
	)

	db.session.add(manufacturer)
	db.session.commit()

	return redirect(url_for("manufacturers"))
