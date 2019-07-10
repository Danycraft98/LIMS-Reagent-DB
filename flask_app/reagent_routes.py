from flask import render_template, url_for, redirect, request
from flask_app import app, db, current_user
from flask_app.models import Reagent, Manufacturer
from flask_app.print import print_label
from datetime import datetime


@app.route("/reagents", methods=['GET', 'POST'])
def reagents():
	if not current_user.logged_in():
		return redirect(url_for('login'))
	all_reagents = Reagent.query.all()
	if request.method == 'POST':
		return render_template("reagent/reagents.html", reagents=Reagent.query.filter_by(name=request.form.get('searchbox')), all_reagents=all_reagents)
	return render_template("reagent/reagents.html", reagents=all_reagents, all_reagents=all_reagents)


@app.route("/reagent/<int:reagent_id>")
def reagent(reagent_id):
	if not current_user.logged_in():
		return redirect(url_for('login'))
	reagent = Reagent.query.get(reagent_id)
	return render_template("reagent/reagent.html", reagent=reagent, Manufacturer=Manufacturer)


@app.route("/add_reagent", methods=["GET", "POST"])
def add_reagent():
	if not current_user.logged_in():
		return redirect(url_for('login'))
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
	if exp_date == '':
		exp_date = None
	elif exp_date:
		exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
	quantity = request.form.get("quantity")

	reagent_label_size = request.form.get('reagent_label_size')
	reagent_label = int(request.form.get('reagent_label'))

	batchpartnum = 1
	while batchpartnum <= reagent_label:
		printcont = (request.form.get("name"), request.form.get("exp_date"), datetime.now())
		print_label(printcont, "reagent", reagent_label_size, None, str(batchpartnum) + '/' + str(reagent_label))
		batchpartnum += 1

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