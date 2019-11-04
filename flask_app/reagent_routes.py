from flask import render_template, url_for, redirect, request
from flask_app import app, db, current_user
from flask_app.models import Reagent, Manufacturer
from flask_app.printer import print_label
from datetime import datetime, timedelta


# Reagent List Route
@app.route("/reagents", methods=['GET', 'POST'])
def reagents():
    # Make sure user is logged in
    if not current_user.logged_in():
        return redirect(url_for('login'))
    all_reagents = Reagent.query.all()

    # Search for specific reagent
    if request.method == 'POST':
        search = request.form.get('searchbox')

        # Search by name
        query_reagents = Reagent.query.filter_by(name=search)
        if query_reagents.count() == 0:
            if len(search.split()) >= 3:
                # Search by UID
                date_searched = datetime.strptime(search.split()[0], "%Y-%m-%d")  # 2019-10-08 14:39:42 1/2
                batch = search.split()[2].split("/")
                query_reagents = Reagent.query.filter(Reagent.date_entered >= date_searched, Reagent.date_entered <= date_searched + timedelta(days=1), Reagent.quantity >= batch[0], Reagent.quantity == batch[1])
            else:
                if "-" in search:
                    # Search by date entered
                    date_searched = datetime.strptime(search, "%Y-%m-%d")  # 2019-10-08
                    query_reagents = Reagent.query.filter(Reagent.date_entered >= date_searched, Reagent.date_entered <= date_searched + timedelta(days=1))
                else:
                    # Search by barcode
                    query_reagents = Reagent.query.filter_by(barcode=search)  # 123456782023-04
        return render_template("reagent/reagents.html", reagents=query_reagents, all_reagents=all_reagents)
    return render_template("reagent/reagents.html", reagents=all_reagents, all_reagents=all_reagents)


# Reagent Route
@app.route("/reagent/<int:reagent_id>", methods=["GET", "POST"])
def reagent(reagent_id):
    # Make sure user is logged in
    if not current_user.logged_in():
        return redirect(url_for('login'))
    reagent = Reagent.query.get(reagent_id)

    # Make sure Reagent is deleted within 24 hours
    deletable = (datetime.today() - reagent.date_entered).total_seconds() < 24 * 3600
    if request.method == 'POST' and deletable:
        db.session.delete(reagent)
        db.session.commit()
        return redirect(url_for('reagents'))
    return render_template("reagent/reagent.html", reagent=reagent, Manufacturer=Manufacturer, range=range(reagent.quantity), deletable=deletable)


# Add Reagent Route
@app.route("/add_reagent", methods=["GET", "POST"])
def add_reagent():
    # Make sure user is logged in
    if not current_user.logged_in():
        return redirect(url_for('login'))
    if request.method == "POST":
        part_num = request.form.get("part_num")
        if part_num == "":
            part_num = -1

        lot_num = request.form.get("lot_num")
        if lot_num == "":
            lot_num = -1

        exp_date = request.form.get("exp_date")
        if exp_date == '':
            exp_date = datetime.today().replace(year=datetime.today().year + 10)
        elif exp_date:
            exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
        quantity = int(request.form.get("quantity"))

        reagent = Reagent(
            name=request.form.get("name"),
            barcode=request.form.get("barcode"),
            part_num=part_num,
            lot_num=lot_num,
            date_entered=datetime.today(),
            exp_date=exp_date,
            quantity=quantity,
            comment=request.values.get("comment"),
            manufacturer_fk=request.values.get("manu_name").split(',')[-1],
        )

        db.session.add(reagent)
        db.session.commit()

        return redirect(url_for("reagents"))

    manu_name = Manufacturer.query.all()
    today = datetime.today().date()
    return render_template("reagent/add_reagent.html", manu_name=manu_name, today=today)


# Print Reagent Redirect
@app.route("/print_reagent/<int:reagent_id>", methods=["GET", "POST"])
def print_reagent(reagent_id):
    reagent = Reagent.query.filter_by(id=reagent_id)[0]

    reagent_label_size = request.form.get('reagent_label_size')
    acquired_stat = request.form.get('acquired_stat')

    batchnum = 1
    while batchnum <= reagent.quantity:
        printcont = (reagent.name, reagent.exp_date, datetime.now())
        print_label(printcont, "reagent", reagent_label_size, acquired_stat, str(batchnum) + '/' + str(reagent.quantity))
        batchnum += 1

    return redirect(url_for("reagent", reagent_id=reagent_id))
