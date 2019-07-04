from flask import render_template, url_for, redirect, request
from flask_app import app, db
from flask_app.models import Manufacturer, MadeReagent, Component
from flask_app.print import print_label
from datetime import datetime


@app.route("/made_reagents")
def made_reagents():
	if request.method == 'POST':
		return redirect(url_for("made_reagent", made_reagent_id=MadeReagent.query.filter_by(name=request.form.get('searchbox'))[0].id))
	made_reagents = MadeReagent.query.all()
	return render_template("made_reagent/made_reagents.html", made_reagents=made_reagents)


@app.route("/made_reagent/<int:made_reagent_id>")
def made_reagent(made_reagent_id):
	made_reagent = MadeReagent.query.get(made_reagent_id)
	return render_template("made_reagent/made_reagent.html", made_reagent=made_reagent, Manufacturer=Manufacturer)


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

	made_reagent = MadeReagent(
		name=request.form.get("made_reagent_name"),
		barcode=request.form.get("made_reagent_barcode"),
		part_num=m_part_num,
		lot_num = m_lot_num,
		date_entered=datetime.today(),
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

	made_reagent_label_size = request.form.get('kit_label_size')
	made_reagent_label = int(request.form.get('kit_label'))
	comp_label_size = request.form.get('comp_label_size')
	comp_label = request.form.get('comp_label')

	batchpartnum = 1
	while batchpartnum <= made_reagent_label:
		printcont = (request.form.get("name"), request.form.get("exp_date"), datetime.now())
		print_label(printcont, "kit", made_reagent_label_size, None, str(batchpartnum) + '/' + str(made_reagent_label))
		batchpartnum += 1

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