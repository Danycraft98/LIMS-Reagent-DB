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


@app.route("/manufacturer_delete/<int:manufacturer_id>")
def manufacturer_delete(manufacturer_id):
	if not current_user.logged_in():
		return redirect(url_for('login'))

	manufacturer = Manufacturer.query.get(manufacturer_id)
	current_time = datetime.today()
	if (current_time - manufacturer.date_entered).total_seconds() > 3 * 3600:
		return redirect(url_for('manufacturer', manufacturer_id=manufacturer_id))
	
	for kit in manufacturer.kits:
		db.session.delete(kit)

	for reagent in manufacturer.reagents:
		db.session.delete(reagent)

	db.session.delete(manufacturer)
	db.session.commit()
	return redirect(url_for('manufacturers'))


@app.route("/add_manufacturer", methods=["GET", "POST"])
def add_manufacturer():
	if not current_user.logged_in():
		return redirect(url_for('login'))
	return render_template("manufacturer/add_manufacturer.html")


@app.route("/add_manufacturer_redirect", methods=["GET", "POST"])
def add_manufacturer_redirect():
	# Request values from html inputs
	barcode = request.form.get('barcode')

	cb = {"part_num":0, "lot_num":0, "exp_date": 0}
	for item in request.form.getlist("cb"):
		cb[item] = 1

	try:
		part_start = int(request.form.get("part_start"))
		part_end = len(request.form.get("part_num")) + part_start
	except Exception:
		part_start = part_end = -1

	try:
		lot_start = int(request.form.get("lot_start"))
		lot_end = len(request.form.get("lot_num")) + lot_start
	except Exception:
		lot_start = lot_end = -1

	try:
		exp_date_start = int(request.form.get("exp_date_start"))
		exp_date_end = exp_date_start + 7
	except Exception:
		exp_date_start = exp_date_end = -1

	compo_barcode = request.form.get('compo_barcode')

	comp_cb = {"barcode": 0, "part_num": 0, "lot_num": 0}
	for i, item in enumerate(request.form.getlist("comp_cb")):
		comp_cb[item] = 1

	comp_part_start = request.form.get("comp_part_start")
	comp_part_num = request.form.get("comp_part_num")
	comp_lot_start = request.form.get("comp_lot_start")
	comp_lot_num = request.form.get("comp_lot_num")
	try:
		comp_part_start = int(comp_part_start)
		comp_part_end = len(comp_part_num) + comp_part_start
	except:
		comp_part_start = comp_part_end = -1

	try:
		comp_lot_start = int(comp_lot_start)
		comp_lot_end = len(comp_lot_num) + comp_lot_start
	except Exception:
		comp_lot_start = comp_lot_end = -1

	manufacturer = Manufacturer(
		name=request.form.get("manu_name"),
		date_entered=datetime.today(),
		exp_date=cb["exp_date"],
		part_num=cb["part_num"],
		lot_num=cb["lot_num"],
		barcode=barcode,
		part_start=part_start,
		part_end=part_end,
		lot_start=lot_start,
		lot_end=lot_end,
		exp_date_start=exp_date_start,
		exp_date_end=exp_date_end,

		compo_barcode=compo_barcode,
		comp_barcode=comp_cb["barcode"],
		comp_part_num=comp_cb["part_num"],
		comp_lot_num=comp_cb["lot_num"],
		comp_part_start=comp_part_start,
		comp_part_end=comp_part_end,
		comp_lot_start=comp_lot_start,
		comp_lot_end= comp_lot_end
	)

	db.session.add(manufacturer)
	db.session.commit()

	return redirect(url_for("manufacturers"))
