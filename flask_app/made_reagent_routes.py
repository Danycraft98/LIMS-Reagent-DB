from flask import render_template, url_for, redirect, request
from flask_app import app, db, current_user
from flask_app.models import Manufacturer, Reagent, MadeReagent, Component
from flask_app.printer import print_label

from collections import Counter
from datetime import datetime


@app.route("/made_reagents", methods=['GET', 'POST'])
def made_reagents():
	if not current_user.logged_in():
		return redirect(url_for('login'))
	all_made_reagents = MadeReagent.query.all()
	if request.method == 'POST':
		return render_template("made_reagent/made_reagents.html", made_reagents=MadeReagent.query.filter_by(name=request.form.get('searchbox')), all_made_reagents=all_made_reagents)
	return render_template("made_reagent/made_reagents.html", made_reagents=all_made_reagents, all_made_reagents=all_made_reagents)


@app.route("/made_reagent/<int:made_reagent_id>")
def made_reagent(made_reagent_id):
	if not current_user.logged_in():
		return redirect(url_for('login'))
	made_reagent = MadeReagent.query.get(made_reagent_id)
	return render_template("made_reagent/made_reagent.html", made_reagent=made_reagent, reagent_list=eval(made_reagent.reagent_list), component_list=eval(made_reagent.component_list), Manufacturer=Manufacturer, Reagent=Reagent, Component=Component)


@app.route("/made_reagent_delete/<int:made_reagent_id>")
def made_reagent_delete(made_reagent_id):
	if not current_user.logged_in():
		return redirect(url_for('login'))
	made_reagent = MadeReagent.query.get(made_reagent_id)
	current_time = datetime.today()
	if (current_time - made_reagent.date_entered).total_seconds() > 24 * 3600:
		return redirect(url_for('made_reagent', made_reagent_id=made_reagent_id))
	db.session.delete(made_reagent)
	db.session.commit()
	return redirect(url_for('made_reagents'))


@app.route("/add_made_reagent", methods=["GET", "POST"])
def add_made_reagent():
	if not current_user.logged_in():
		return redirect(url_for('login'))
	comp_infos = {}
	for comp in Component.query.all():
		comp_infos[comp.barcode] = comp.name

	for reagent in Reagent.query.all():
		comp_infos[reagent.barcode] = reagent.name
	today = datetime.today().date()
	return render_template("made_reagent/add_made_reagent.html", today=today, comp_infos=comp_infos)


@app.route("/add_made_reagent_redirect", methods=["GET", "POST"])
def add_made_reagent_redirect():
	exp_date = request.form.get("exp_date")
	if exp_date == '':
		exp_date = None
	elif exp_date:
		exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
	quantity = int(request.form.get("quantity"))

	made_reagent = MadeReagent(
		name=request.form.get("name"),
		exp_date = exp_date,
		date_entered=datetime.today(),
		quantity = quantity
	)

	db.session.add(made_reagent)
	db.session.commit()

	names = Counter(request.form.getlist("comp_name"))

	made_reagent_label_size = request.form.get('made_reagent_label_size')
	made_reagent_label = int(request.form.get('made_reagent_label'))
	comp_label_s = int(request.form.get('comp_label_s'))
	comp_label_m = int(request.form.get('comp_label_m'))
	acquired_stat = request.form.get('acquired_stat')

	batchnum = 1
	batchpartnum = 1
	while batchnum <= made_reagent_label:
		printcont = (request.form.get("name"), exp_date, datetime.now())
		print_label(printcont, "made reagent", made_reagent_label_size, acquired_stat, str(batchpartnum) + '/' + str(made_reagent_label))
		batchpartnum += 1
		if batchpartnum > quantity:
			batchpartnum = 1
		batchnum += 1

	reagent_list = {}
	component_list = {}
	for name in names:
		batchnum = 1
		batchpartnum = 1
		while batchnum <= comp_label_s:
			printcont = (name, exp_date, datetime.now())
			print_label(printcont, "made reagent", "s", acquired_stat, str(batchpartnum) + '/' + str(quantity))
			batchpartnum += 1
			if batchpartnum > quantity:
				batchpartnum = 1
			batchnum += 1

		batchnum = 1
		batchpartnum = 1
		while batchnum <= comp_label_m:
			printcont = (name, exp_date, datetime.now())
			print_label(printcont, "made reagent", "m", acquired_stat, str(batchpartnum) + '/' + str(quantity))
			batchpartnum += 1
			if batchpartnum > quantity:
				batchpartnum = 1
			batchnum += 1

		#
		if len(list(Reagent.query.filter_by(name=name))) > 0:
			reagent_list[name] = names[name]
		elif len(list(Component.query.filter_by(name=name))) > 0:
			component_list[name] = names[name]
	made_reagent.reagent_list = str(reagent_list)
	made_reagent.component_list = str(component_list)
	db.session.commit()

	return redirect(url_for("made_reagents"))


@app.route("/print_made_reagent/<int:made_reagent_id>", methods=["GET", "POST"])
def print_made_reagent(made_reagent_id):
	return redirect(url_for("made_reagent", made_reagent_id=made_reagent_id))