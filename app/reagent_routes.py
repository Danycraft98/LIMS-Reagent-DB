from flask import render_template, url_for, redirect, request
from flask_login import login_required
from datetime import datetime

from app import app, db
from app.models import Reagent, Manufacturer
from app.printer import print_label
from app.route import current_user


# Reagent Route
@app.route("/reagent/<int:reagent_id>", methods=["GET", "POST"])
@login_required
def reagent(reagent_id):
    reagent1 = Reagent.query.get(reagent_id)
    if not reagent1:
        return render_template('404.html'), 404

    # Make sure Reagent is deleted within 24 hours
    deletable = (datetime.now() - reagent1.date_entered).total_seconds() < 24 * 3600
    if request.method == 'POST':
        reagent1.comment = request.form.get("comment")
        db.session.merge(reagent1)
        db.session.commit()
    return render_template("reagent/reagent.html", reagent=reagent1, Manufacturer=Manufacturer, range=range(reagent1.quantity), deletable=deletable)


# Add Reagent Route
@app.route("/add_reagent", methods=["GET", "POST"])
@login_required
def add_reagent():
    if request.method == "POST":
        form = request.form
        try:
            exp_date = datetime.strptime(form.get("exp_date"), "%Y-%m-%d")
        except ValueError:
            exp_date = None

        try:
            date_tested = datetime.strptime(form.get("date_tested"), "%Y-%m-%d")
        except ValueError:
            date_tested = None

        new_reagent = Reagent(
            name=request.form.get("name"),
            manufacturer_id=request.values.get("manu_name").split(',')[0],
            barcode=request.form.get("barcode"),
            part_num=form.get("part_num"),
            lot_num=form.get("lot_num"),
            exp_date=exp_date,
            date_entered=datetime.now(),
            date_tested=date_tested,
            p_num=request.form.get('p_num'),
            quantity=int(request.form.get("quantity")),
            comment=request.values.get("comment"),
            user_id=current_user.id
        )

        db.session.add(new_reagent)
        db.session.commit()

        return redirect(url_for("reagent", reagent_id=new_reagent.id))

    manufacturers = Manufacturer.query.all()
    reagents = Reagent.query.all()
    today = datetime.now().date()
    return render_template("reagent/add_reagent.html", manufacturers=manufacturers, today=today, reagents=reagents)


# Print Reagent Redirect
@app.route("/print_reagent/<int:reagent_id>", methods=["GET", "POST"])
@login_required
def print_reagent(reagent_id):
    reagent1 = Reagent.query.filter_by(id=reagent_id)[0]

    reagent_label_size = request.form.get('reagent_label_size')
    acquired_stat = request.form.get('acquired_stat')

    batchnum = 1
    while batchnum <= reagent1.quantity:
        printcont = (reagent1.name, reagent1.exp_date, datetime.now())
        print_label(printcont, "reagent", reagent_label_size, acquired_stat, str(batchnum) + '/' + str(reagent1.quantity))
        batchnum += 1

    return redirect(url_for("reagent", reagent_id=reagent_id))
