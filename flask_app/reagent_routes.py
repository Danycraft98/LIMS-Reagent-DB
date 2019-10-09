from flask import render_template, url_for, redirect, request
from flask_app import app, db, current_user
from flask_app.models import Reagent, Manufacturer
from flask_app.printer import print_label
from datetime import datetime


@app.route("/reagents", methods=['GET', 'POST'])
def reagents():
    if not current_user.logged_in():
        return redirect(url_for('login'))
    all_reagents = Reagent.query.all()
    if request.method == 'POST':
        return render_template("reagent/reagents.html",
                               reagents=Reagent.query.filter_by(name=request.form.get('searchbox')),
                               all_reagents=all_reagents)
    return render_template("reagent/reagents.html", reagents=all_reagents, all_reagents=all_reagents)


@app.route("/reagent/<int:reagent_id>")
def reagent(reagent_id):
    if not current_user.logged_in():
        return redirect(url_for('login'))
    reagent = Reagent.query.get(reagent_id)
    return render_template("reagent/reagent.html", reagent=reagent, Manufacturer=Manufacturer,
                           range=range(reagent.quantity))


@app.route("/reagent_delete/<int:reagent_id>")
def reagent_delete(reagent_id):
    if not current_user.logged_in():
        return redirect(url_for('login'))
    reagent = Reagent.query.get(reagent_id)
    current_time = datetime.today()
    if (current_time - reagent.date_entered).total_seconds() > 24 * 3600:
        return redirect(url_for('reagent', reagent_id=reagent_id))
    db.session.delete(reagent)
    db.session.commit()
    return redirect(url_for('reagents'))


@app.route("/add_reagent", methods=["GET", "POST"])
def add_reagent():
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
            exp_date = None
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


@app.route("/print_reagent/<int:reagent_id>", methods=["GET", "POST"])
def print_reagent(reagent_id):
    reagent = Reagent.query.filter_by(id=reagent_id)[0]

    reagent_label_size = request.form.get('reagent_label_size')
    reagent_label = int(request.form.get('reagent_label'))
    acquired_stat = request.form.get('acquired_stat')

    batchpartnum = 1
    batchnum = 1
    while batchnum <= reagent_label:
        printcont = (request.form.get("name"), reagent.exp_date, datetime.now())
        print_label(printcont, "reagent", reagent_label_size, acquired_stat,
                    str(batchpartnum) + '/' + str(reagent.quantity))
        batchpartnum += 1
        if batchpartnum > reagent.quantity:
            batchpartnum = 1
        batchnum += 1
    return redirect(url_for("reagent", reagent_id=reagent_id))
