from flask import render_template, url_for, redirect, request
from flask_app import app, db
from flask_app.models import *
from datetime import datetime


@app.route("/made_reagents")
def made_reagents():
	made_reagents = Kit.query.all()
	return render_template("made_reagent/made_reagents.html", made_reagents=made_reagents)


@app.route("/made_reagent/<int:made_reagent_id>")
def made_reagent(made_reagent_id):
	made_reagent = Kit.query.get(made_reagent_id)
	return render_template("made_reagent/made_reagent.html", made_reagent=made_reagent)


@app.route("/add_made_reagent", methods=["GET", "POST"])
def add_made_reagent():
	manu_name = Manufacturer.query.all()
	return render_template("made_reagent/add_made_reagent.html", title="Add", manu_name=manu_name)


@app.route("/add_made_reagent_redirect", methods=["GET", "POST"])
def add_made_reagent_redirect():
	manu_id = Manufacturer.query.filter_by(name=request.form.get("manu_name")).first().id
	try:
		m_part_num = int(request.form.get("made_reagent_part_num"))
	except:
		m_part_num = -1

	try:
		m_lot_num = int(request.form.get("made_reagent_lot_num"))
	except:
		m_lot_num = -1

	exp_date = request.form.get("exp_date")
	if exp_date == "":
		exp_date = None
	quantity = request.form.get("quantity")

	made_reagent = Kit(
		name=request.form.get("made_reagent_name"),
		barcode=request.form.get("made_reagent_barcode"),
		part_num=m_part_num,
		lot_num = m_lot_num,
		exp_date = datetime.strptime(exp_date, "%Y-%m-%d"),
		quantity = quantity,
		manufacturer_fk = manu_id,
	)

	db.session.add(made_reagent)
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
			made_reagent_fk=made_reagent.id
		)
		db.session.add(component)
		db.session.commit()

	return redirect(url_for("made_reagents"))