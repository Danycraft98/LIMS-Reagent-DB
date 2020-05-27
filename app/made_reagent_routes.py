from flask import render_template, url_for, redirect, request
from flask_login import login_required
from datetime import datetime

from app import app, db
from app.models import Manufacturer, Reagent, MadeReagent, MadeReagentToComp, Component
from app.printer import print_label
from app.route import current_user



@app.route("/made_reagent/<int:made_reagent_id>", methods=["GET", "POST"])
@login_required
def made_reagent(made_reagent_id):
    made_reagent1 = MadeReagent.query.get(made_reagent_id)
    if not made_reagent1:
        return render_template('404.html'), 404

    # Make sure Reagent is deleted within 24 hours
    deletable = (datetime.now() - made_reagent1.date_entered).total_seconds() < 24 * 3600
    if request.method == 'POST':
        made_reagent1.comment = request.form.get("comment")
        db.session.merge(made_reagent1)
        db.session.commit()
        return redirect(url_for("made_reagent", made_reagent_id=made_reagent_id))
    return render_template("made_reagent/made_reagent.html", made_reagent=made_reagent1, eval=eval, Manufacturer=Manufacturer, Reagent=Reagent, Component=Component, deletable=deletable)


@app.route("/add_made_reagent", methods=["GET", "POST"])
@login_required
def add_made_reagent():
    if request.method == "POST":
        exp_date = request.form.get("exp_date")
        if exp_date == '':
            exp_date = None
        elif exp_date:
            exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
        quantity = int(request.form.get("quantity"))

        date_tested = request.form.get("date_tested")
        if date_tested == '':
            date_tested = None
        elif date_tested:
            date_tested = datetime.strptime(date_tested, "%Y-%m-%d")

        made_reagent_ = MadeReagent(
            name=request.form.get("name"),
            exp_date=exp_date,
            date_entered=datetime.now(),
            quantity=quantity,
            date_tested=date_tested,
            p_num=request.form.get('p_num'),
            comment=request.values.get("comment"),
            user_id=current_user.id
        )

        db.session.add(made_reagent_)
        db.session.commit()

        names = request.form.getlist("comp_name")
        is_first = True
        for name in names:
            if is_first:
                is_first = False
                continue
            reagents = Reagent.query.filter_by(name=name)
            components = Component.query.filter_by(name=name)
            made_reagent_to_comp = None
            if reagents.count() > 0:
                made_reagent_to_comp = MadeReagentToComp(madereagent_id=made_reagent_.id, reagent_id=reagents.first().id)
            elif components.count() > 0:
                made_reagent_to_comp = MadeReagentToComp(madereagent_id=made_reagent_.id, comp_id=components.first().id)

            if made_reagent_to_comp:
                db.session.add(made_reagent_to_comp)
                db.session.commit()
        db.session.commit()

        return redirect(url_for("made_reagent", made_reagent_id=made_reagent_.id))

    comp_infos = {}
    for comp in Component.query.all():
        comp_infos[comp.barcode] = comp.name

    for reagent in Reagent.query.all():
        comp_infos[reagent.barcode] = reagent.name
    today = datetime.now().date()
    made_reagents = MadeReagent.query.all()
    return render_template("made_reagent/add_made_reagent.html", add_comp=True, today=today, comp_infos=comp_infos, made_reagents=made_reagents, MadeReagentToComp=MadeReagentToComp)


@app.route("/print_made_reagent/<int:made_reagent_id>", methods=["GET", "POST"])
@login_required
def print_made_reagent(made_reagent_id):
    made_reagent_ = MadeReagent.query.filter_by(id=made_reagent_id)[0]

    made_reagent_label_size = request.form.get('made_reagent_label_size')
    acquired_stat = request.form.get('acquired_stat')

    batchnum = 1
    while batchnum <= made_reagent_.quantity:
        printcont = (made_reagent_.name, made_reagent_.exp_date, made_reagent_.date_entered)
        print_label(printcont, "made reagent", made_reagent_label_size, acquired_stat, made_reagent_.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(batchnum) + '/' + str(made_reagent_.quantity))
        batchnum += 1

    return redirect(url_for("made_reagent", made_reagent_id=made_reagent_id))
