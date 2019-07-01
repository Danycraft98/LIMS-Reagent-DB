from flask import render_template, url_for, redirect, request
from flask_app import app
from flask_app.models import *
from datetime import datetime


@app.route("/reagents")
def reagents():
	reagents = Reagent.query.all()
	return render_template("reagent/reagents.html", reagents=reagents)


@app.route("/reagent/<int:reagent_id>")
def reagent(reagent_id):
	reagent = Reagent.query.get(reagent_id)
	return render_template("reagent/reagent.html", reagent=reagent, Manufacturer=Manufacturer)


@app.route("/add_reagent", methods=["GET", "POST"])
def add_reagent():
	manu_name = Manufacturer.query.all()
	return render_template("reagent/add_reagent.html", manu_name=manu_name)


@app.route("/add_reagent_redirect", methods=["GET", "POST"])
def add_reagent_redirect():
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

	reagent = Reagent(
		name=request.form.get("name"),
		barcode=request.form.get("barcode"),
		part_num=part_num,
		lot_num = lot_num,
		date_entered=datetime.today(),
		exp_date = exp_date,
		quantity = quantity,
		manufacturer_fk = manu_id,
	)

	db.session.add(reagent)
	db.session.commit()

	return redirect(url_for("reagents"))