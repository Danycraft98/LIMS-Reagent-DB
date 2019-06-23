from flask import render_template, url_for, redirect, request
from flask_app import engine_RK, app



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
	with engine_RK.connect() as con:
		kits = con.execute(
			'SELECT * FROM kit_master;')
	for row in kits:
		print(row)
	return render_template('home.html')


@app.route("/manufacturer")
def manufacturer():
	with engine_RK.connect() as con:
		manu_info = con.execute('SELECT * FROM manu_info;')
	return render_template('manufacturer.html', title='manufacturer', manu_info=manu_info)


@app.route("/add_manufacturer", methods=['GET', 'POST'])
def add_manufacturer():
	return render_template('add_manufacturer.html', title='Add')


@app.route("/add_manufacturer_redirect", methods=['GET', 'POST'])
def add_manufacturer_redirect():
	# Request values from html inputs
	name = request.form.get('name_m')
	components = request.form.getlist('name_c')
	manufacturer = request.form.get('manufacturer')
	boxlots = request.form.get('boxlot')
	comp_num = request.form.getlist('compnum')
	part_num = request.form.getlist('partnum')
	lot_num = request.form.getlist('lotnum')
	lab_date = request.form.getlist('labexp')
	copynum = request.form.get('copynum')
	comp_coms = request.form.getlist('compnote_comment')
	comp_stats = request.form.getlist('compnote_status')
	cons = request.form.getlist('condition')

	with engine_RK.connect() as con:
		con.execute('INSERT INTO kit_master (Name_Master) VALUES (%s);', (name))
		kit_item = con.execute('SELECT ID FROM kit_master WHERE Name_Master=%s;', (name))



		for row in kit_item:
			id = int(row[0])
			for component in components:
				con.execute('INSERT INTO kit_comp (Name_Comp, master_link) VALUES (%s, %s);', (component, id))

	return redirect(url_for('manufacturer'))


@app.route("/kit")
def kit():
	return render_template('kit.html', title='Kit')


@app.route("/add_kit", methods=['GET', 'POST'])
def kit_add():
	return render_template('add_kit.html', title='Add')


@app.route("/add_kit_redirect", methods=['GET', 'POST'])
def add_kit_redirect():
	# Request values from html inputs
	name = request.form.get('name_m')
	components = request.form.getlist('name_c')
	manufacturer = request.form.get('manufacturer')
	boxlots = request.form.get('boxlot')
	comp_num = request.form.getlist('compnum')
	part_num = request.form.getlist('partnum')
	lot_num = request.form.getlist('lotnum')
	lab_date = request.form.getlist('labexp')
	copynum = request.form.get('copynum')
	comp_coms = request.form.getlist('compnote_comment')
	comp_stats = request.form.getlist('compnote_status')
	cons = request.form.getlist('condition')

	with engine_RK.connect() as con:
		con.execute('INSERT INTO kit_master (Name_Master) VALUES (%s);', (name))
		kit_item = con.execute('SELECT ID FROM kit_master WHERE Name_Master=%s;', (name))

		for row in kit_item:
			print(row)
			id = int(row[0])

	return redirect(url_for('kit'))


@app.route("/reagent")
def reagent():
	return render_template('reagent.html', title='Reagent')


@app.route("/add_reagent", methods=['GET', 'POST'])
def reagent_add():
	return render_template('add_reagent.html', title='Add')


@app.route("/made-reagent")
def made_reagent():
	return render_template('made-reagent.html', title='Made Reagent')


@app.route("/add_made-reagent", methods=['GET', 'POST'])
def made_reagent_add():
	return render_template('add_made-reagent.html', title='Add')


@app.route("/addition", methods=['GET', 'POST'])
def addition():
	# Request values from html inputs
	name = request.form.get('name_m')
	components = request.form.getlist('name_c')
	manufacturer = request.form.get('manufacturer')
	boxlots = request.form.get('boxlot')
	comp_num = request.form.getlist('compnum')
	part_num = request.form.getlist('partnum')
	lot_num = request.form.getlist('lotnum')
	lab_date = request.form.getlist('labexp')
	copynum = request.form.get('copynum')
	comp_coms = request.form.getlist('compnote_comment')
	comp_stats = request.form.getlist('compnote_status')
	cons = request.form.getlist('condition')

	with engine_RK.connect() as con:
		con.execute('INSERT INTO kit_master (Name_Master) VALUES (%s);', (name))
		kit_item = con.execute('SELECT ID FROM kit_master WHERE Name_Master=%s;', (name))

		for row in kit_item:
			id = int(row[0])

	return redirect(url_for('kit'))