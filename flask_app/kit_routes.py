from wtforms import Form, StringField, SelectField
from flask import render_template, url_for, redirect, request
from flask_app import app
from flask_app.models import *
from datetime import datetime
from flask_app.print import print_label


class MusicSearchForm(Form):
	search = StringField('')


@app.route("/kits", methods=['GET', 'POST'])
def kits():
	if request.method == 'POST':
		return redirect(url_for("kit", kit_id=Kit.query.filter_by(name=request.form.get('searchbox'))[0].id))
	kits = Kit.query.all()
	return render_template("kit/kits.html", kits=kits)


@app.route("/kit/<int:kit_id>")
def kit(kit_id):
	kit = Kit.query.get(kit_id)
	return render_template("kit/kit.html", kit=kit, Manufacturer=Manufacturer)


@app.route("/add_kit", methods=["GET", "POST"])
def add_kit():
	manu_name = Manufacturer.query.all()
	if request.method == 'POST':
		if request.form.get('print') == 'print':
			comp_names = request.form.getlist("comp_name")

			kit_label_size = request.form.get('kit_label_size')
			kit_label = int(request.form.get('kit_label'))
			comp_label_size = request.form.get('comp_label_size')
			comp_label = request.form.get('comp_label')

			batchpartnum = 1
			while batchpartnum <= kit_label:
				printcont = (request.form.get("name"), request.form.get("exp_date"), datetime.now())
				print_label(printcont, "kit", kit_label_size, None, str(batchpartnum) + '/' + str(kit_label))
				batchpartnum += 1

			for name in comp_names:
				batchpartnum = 1
				while batchpartnum <= kit_label:
					printcont = (name, request.form.get("exp_date"), datetime.now())
					print_label(printcont, "kit", comp_label_size, None, str(batchpartnum) + '/' + str(comp_label))
					batchpartnum += 1

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