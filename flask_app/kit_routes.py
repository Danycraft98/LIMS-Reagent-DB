from flask import render_template, url_for, redirect, request
from flask_app import app, db
from flask_app.models import *
from datetime import datetime


@app.route("/kits")
def kits():
	kits = Kit.query.all()
	return render_template("kit/kits.html", title="Kit", kits=kits)


@app.route("/kit/<int:kit_id>")
def kit(kit_id):
	kit = Kit.query.get(kit_id)
	return render_template("kit/kit.html", title="Kit", kit=kit)


@app.route("/add_kit", methods=["GET", "POST"])
def add_kit():
	manu_name = Manufacturer.query.all()
	return render_template("kit/add_kit.html", title="Add", manu_name=manu_name)


@app.route("/add_kit_redirect", methods=["GET", "POST"])
def add_kit_redirect():
	manu_name = request.form.get("manu_name")
	kit_barcode = request.form.get("kit_barcode")
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
		manufacturer_fk = 1,
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

	return redirect(url_for("kits"))