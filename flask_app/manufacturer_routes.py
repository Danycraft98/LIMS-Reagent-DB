from flask import render_template, url_for, redirect, request
from flask_app import app, db
from flask_app.models import Manufacturer


@app.route("/manufacturers")
def manufacturers():
	manufacturers = Manufacturer.query.all()
	return render_template("manufacturer/manufacturers.html", manufacturers=manufacturers)


@app.route("/manufacturer/<int:manufacturer_id>")
def manufacturer(manufacturer_id):
	manufacturer = Manufacturer.query.get(manufacturer_id)
	return render_template("manufacturer/manufacturer.html", manufacturer=manufacturer)


@app.route("/add_manufacturer", methods=["GET", "POST"])
def add_manufacturer():
	return render_template("manufacturer/add_manufacturer.html", title="Add")


@app.route("/add_manufacturer_redirect", methods=["GET", "POST"])
def add_manufacturer_redirect():
	# Request values from html inputs
	kit_cb = {"part_num":0, "lot_num":0, "exp_date": 0}
	for item in request.form.getlist("kit_cb"):
		kit_cb[item] = 1

	try:
		kit_part_start = int(request.form.get("kit_part_start"))
		kit_part_end = len(request.form.get("kit_part_num")) + kit_part_start
	except:
		kit_part_start = kit_part_end = -1

	try:
		kit_lot_start = int(request.form.get("kit_lot_start"))
		kit_lot_end = len(request.form.get("kit_lot_num")) + kit_lot_start
	except:
		kit_lot_start = kit_lot_end = -1

	comp_cb = {"barcode":0,"part_num": 0, "lot_num": 0}
	for item in request.form.getlist("comp_cb"):
		comp_cb[item] = 1

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

	manufacturer = Manufacturer(
		name = request.form.get("manu_name"),
		exp_date = kit_cb["exp_date"],
		kit_part_num = kit_cb["part_num"],
		kit_lot_num = kit_cb["lot_num"],
		kit_part_start = kit_part_start,
		kit_part_end = kit_part_end,
		kit_lot_start = kit_lot_start,
		kit_lot_end = kit_lot_end,
		comp_barcode = comp_cb["barcode"],
		part_num = comp_cb["part_num"],
		lot_num = comp_cb["lot_num"],
		part_start = part_start,
		part_end = part_end,
		lot_start = lot_start,
		lot_end = lot_end
	)

	db.session.add(manufacturer)
	db.session.commit()

	return redirect(url_for("manufacturer"))
