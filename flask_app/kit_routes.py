from flask import render_template, url_for, redirect, request
from flask_app import app
from flask_app.models import *
from datetime import datetime


@app.route("/kits")
def kits():
	kits = Kit.query.all()
	return render_template("kit/kits.html", kits=kits)


@app.route("/kit/<int:kit_id>")
def kit(kit_id):
	kit = Kit.query.get(kit_id)
	return render_template("kit/kit.html", kit=kit, Manufacturer=Manufacturer)


@app.route("/add_kit", methods=["GET", "POST"])
def add_kit():
	manu_name = Manufacturer.query.all()
	return render_template("kit/add_kit.html", title="Add", manu_name=manu_name)


@app.route("/add_kit_redirect", methods=["GET", "POST"])
def add_kit_redirect():
	manu_id = Manufacturer.query.filter_by(name=request.values.get("manu_name").split(",")[-1]).first().id
	try:
		part_num = int(request.form.get("part_num"))
	except:
		part_num = -1

	try:
		lot_num = int(request.form.get("lot_num"))
	except:
		lot_num = -1

	exp_date = request.form.get("exp_date")
	if exp_date:
		exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
	quantity = request.form.get("quantity")

	kit = Kit(
		name=request.form.get("name"),
		barcode=request.form.get("barcode"),
		part_num=part_num,
		lot_num = lot_num,
		date_entered = datetime.today(),
		exp_date =  exp_date,
		quantity = quantity,
		manufacturer_fk = manu_id,
	)

	db.session.add(kit)
	db.session.commit()

	names = request.form.getlist("comp_name")
	comp_nums = request.form.getlist("comp_barcode")
	comp_part_nums = request.form.getlist("comp_part_num")
	comp_lot_nums = request.form.getlist("comp_lot_num")
	conditions = request.form.getlist("condition")

	for name, comp_num, part_num, lot_num, condition in zip(names, comp_nums, comp_part_nums, comp_lot_nums, conditions):
		component = Component(
			name=name,
			barcode=comp_num,
			part_num=part_num,
			lot_num=lot_num,
			condition=condition,
			kit_fk=kit.id,
			madereagent_fk=None
		)
		db.session.add(component)
		db.session.commit()

	return redirect(url_for("kits"))