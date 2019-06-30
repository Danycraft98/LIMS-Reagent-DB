from flask import render_template, url_for, redirect, request
from flask_app import app, db
from flask_app.models import *
from datetime import datetime


@app.route("/reagents")
def reagents():
	kits = Kit.query.all()
	return render_template("reagent/reagents.html", kits=kits)


@app.route("/reagent/<int:reagent_id>")
def reagent(reagent_id):
	kit = Kit.query.get(reagent_id)
	return render_template("reagent/reagent.html", kit=kit)


@app.route("/add_reagent", methods=["GET", "POST"])
def add_reagent():
	manu_name = Manufacturer.query.all()
	return render_template("reagent/add_reagent.html", manu_name=manu_name)


@app.route("/add_reagent_redirect", methods=["GET", "POST"])
def add_reagent_redirect():
	manu_id = Manufacturer.query.filter_by(name=request.form.get("manu_name")).first().id
	try:
		m_part_num = int(request.form.get("kit_part_num"))
	except:
		m_part_num = -1

	try:
		m_lot_num = int(request.form.get("kit_lot_num"))
	except:
		m_lot_num = -1

	exp_date = request.form.get("exp_date")
	if exp_date == "":
		exp_date = None
	quantity = request.form.get("quantity")

	kit = Kit(
		name=request.form.get("kit_name"),
		barcode=request.form.get("kit_barcode"),
		part_num=m_part_num,
		lot_num = m_lot_num,
		exp_date = datetime.strptime(exp_date, "%Y-%m-%d"),
		quantity = quantity,
		manufacturer_fk = manu_id,
	)

	db.session.add(kit)
	db.session.commit()

	names = request.form.getlist("comp_name")
	comp_nums = request.form.getlist("comp_barcode")
	part_nums = request.form.getlist("part_num")
	lot_nums = request.form.getlist("lot_num")
	conditions = request.form.getlist("condition")

	for name, comp_num, part_num, lot_num, condition in zip(names, comp_nums, part_nums, lot_nums, conditions):
		component = Component(
			name=name,
			barcode=comp_num,
			part_num=part_num,
			lot_num=lot_num,
			condition=condition,
			kit_fk=kit.id
		)
		db.session.add(component)
		db.session.commit()

	return redirect(url_for("reagents"))