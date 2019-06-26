from flask import render_template, url_for, redirect, request
from flask_app import engine_RK, app
from flask_app.forms import *



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
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
	manu_name = request.form.get('manu_name')
	if 'exp_date' in request.form.getlist('master_cb'):
		master_exp_date_cb = 1
	else:
		master_exp_date_cb = 0

	try:
		master_part_start = int(request.form.get('master_part_start'))
		master_part_end = len(request.form.get('master_part_num')) + master_part_start
	except:
		master_part_start = master_part_end = -1

	try:
		master_lot_start = int(request.form.get('master_lot_start'))
		master_lot_end = len(request.form.get('master_lot_num')) + master_lot_start
	except:
		master_lot_start = master_lot_end = -1

	if 'comp_lot' in request.form.getlist('comp_cb'):
		exp_date_cb = 1
	else:
		exp_date_cb = 0

	try:
		part_start = int(request.form.get('part_start'))
		part_end = len(request.form.get('part_num')) + part_start
	except:
		part_start = part_end = -1

	try:
		lot_start = int(request.form.get('lot_start'))
		lot_end = len(request.form.get('lot_end')) + lot_start
	except:
		lot_start = lot_end = -1

	with engine_RK.connect() as con:
		con.execute('INSERT INTO manu_info (manu_name,master_exp_date, master_part_start, master_part_end, master_lot_start,  master_lot_end, part_start, part_end, lot_start,  lot_end) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (manu_name, master_exp_date_cb, master_part_start, master_part_end, master_lot_start, master_lot_end, part_start, part_end, lot_start, lot_end))

	return redirect(url_for('manufacturer'))


@app.route("/kit")
def kits():
	with engine_RK.connect() as con:
		kit_master = con.execute('SELECT * FROM kit_master;')
	return render_template('kits.html', title='Kit', kit_master=kit_master)


@app.route("/kit/<int:kit_id>")
def kit(kit_id):
	with engine_RK.connect() as con:
		kit_master = con.execute('SELECT * FROM kit_master WHERE id=%s;', kit_id)
		print(kit_master)
	return render_template('kits.html', title='Kit')


@app.route("/add_kit", methods=['GET', 'POST'])
def add_kit():
	with engine_RK.connect() as con:
		manu_name = con.execute('SELECT manu_name FROM manu_info;')
	return render_template('add_kit.html', title='Add', manu_name=manu_name)


@app.route("/add_kit_redirect", methods=['GET', 'POST'])
def add_kit_redirect():
	# Request values from html inputs
	kit_name = request.form.get('master_name')
	manu_name = request.form.get('manu_name')
	box_lot_barcode = request.form.get('master_barcode')
	try:
		m_part_num = int(request.form.get('master_part_num'))
	except:
		m_part_num = -1

	try:
		m_lot_num = int(request.form.get('master_lot_num'))
	except:
		m_lot_num = -1

	expiry_date = request.form.getlist('expiry_date')


	components = request.form.getlist('comp_name')
	comp_num = request.form.getlist('compnum')
	part_num = request.form.getlist('partnum')
	lot_num = request.form.getlist('lotnum')
	copynum = request.form.get('copynum')
	comp_coms = request.form.getlist('compnote_comment')
	comp_stats = request.form.getlist('compnote_status')
	cons = request.form.getlist('condition')

	with engine_RK.connect() as con:
		manu_id = con.execute('SELECT ID FROM manu_info WHERE manu_name=%s;', (manu_name))
		con.execute('INSERT INTO kit_master (kit_name, box_lot_barcode, part_num, lot_num, expiry_date) VALUES (%s, %s, %s, %s, %s);', (kit_name, box_lot_barcode, m_part_num, m_lot_num, expiry_date))

	return redirect(url_for('kits'))


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