from flask import render_template, url_for, redirect, request
from flask_app import app, db, current_user
from flask_app.models import Kit, Manufacturer, Component
from datetime import datetime
from flask_app.printer import print_label


@app.route("/kits", methods=['GET', 'POST'])
def kits():
	if not current_user.logged_in():
		return redirect(url_for('login'))
	all_kits = Kit.query.all()
	if request.method == 'POST':
		return render_template("kit/kits.html", kits=Kit.query.filter_by(name=request.form.get('searchbox')), all_kits=all_kits)
	return render_template("kit/kits.html", kits=all_kits, all_kits=all_kits)


@app.route("/kit/<int:kit_id>")
def kit(kit_id):
	if not current_user.logged_in():
		return redirect(url_for('login'))
	kit = Kit.query.get(kit_id)
	return render_template("kit/kit.html", kit=kit, Manufacturer=Manufacturer)


@app.route("/kit_delete/<int:kit_id>")
def kit_delete(kit_id):
	if not current_user.logged_in():
		return redirect(url_for('login'))
	kit = Kit.query.get(kit_id)
	current_time = datetime.today()
	if (current_time - kit.date_entered).total_seconds() > 3*3600:
		return redirect(url_for('kit', kit_id=kit_id))
	db.session.delete(kit)
	db.session.commit()
	return redirect(url_for('kits'))


@app.route("/add_kit", methods=["GET", "POST"])
def add_kit():
	if not current_user.logged_in():
		return redirect(url_for('login'))
	manu_name = Manufacturer.query.all()
	today = datetime.today().date()
	return render_template("kit/add_kit.html", title="Add", manu_name=manu_name, today=today)


@app.route("/add_kit_redirect", methods=["GET", "POST"])
def add_kit_redirect():
	part_num = request.form.get("part_num")
	if part_num == "":
		part_num = -1

	lot_num = request.form.get("lot_num")
	if lot_num == "":
		lot_num = -1

	exp_date = request.form.get("exp_date")
	if exp_date == "":
		exp_date = None
	elif exp_date:
		exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
	quantity = int(request.form.get("quantity"))

	kit = Kit(
		name=request.form.get("name"),
		barcode=request.form.get("barcode"),
		part_num=part_num,
		lot_num=lot_num,
		date_entered=datetime.today(),
		exp_date=exp_date,
		quantity=quantity,
		manufacturer_fk=request.values.get("manu_name").split(",")[-1],
	)

	db.session.add(kit)
	db.session.commit()

	names = request.form.getlist("comp_name")
	comp_nums = request.form.getlist("comp_barcode")
	comp_part_nums = request.form.getlist("comp_part_num")
	comp_lot_nums = request.form.getlist("comp_lot_num")
	conditions = request.form.getlist("condition")

	kit_label_size = request.form.get('kit_label_size')
	kit_label = int(request.form.get('kit_label'))
	comp_label_s = int(request.form.get('comp_label_s'))
	comp_label_m = int(request.form.get('comp_label_m'))

	batchnum = 1
	batchpartnum = 1
	while batchnum <= kit_label:
		printcont = (request.form.get("name"), exp_date, datetime.now())
		print_label(printcont, "kit", kit_label_size, None, str(batchpartnum) + '/' + str(kit_label))
		batchpartnum += 1
		if batchpartnum > quantity:
			batchpartnum = 1
		batchnum += 1

	for name, comp_num, part_num, lot_num, condition in zip(names, comp_nums, comp_part_nums, comp_lot_nums, conditions):
		batchnum = 1
		batchpartnum = 1
		while batchnum <= comp_label_s:
			printcont = (name, exp_date, datetime.now())
			print_label(printcont, "kit", "s", None, str(batchpartnum) + '/' + str(comp_label_s))
			batchpartnum += 1
			if batchpartnum > quantity:
				batchpartnum = 1
			batchnum += 1

		batchnum = 1
		batchpartnum = 1
		while batchnum <= comp_label_m:
			printcont = (name, exp_date, datetime.now())
			print_label(printcont, "kit", "m", None, str(batchpartnum) + '/' + str(comp_label_m))
			batchpartnum += 1
			if batchpartnum > quantity:
				batchpartnum = 1
			batchnum += 1

		component = Component(
			name=name,
			barcode=comp_num,
			part_num=part_num,
			lot_num=lot_num,
			condition=condition,
			copies=0,
			kit_fk=kit.id,
			madereagent_fk=None
		)
		db.session.add(component)
		db.session.commit()

	return redirect(url_for("kits"))