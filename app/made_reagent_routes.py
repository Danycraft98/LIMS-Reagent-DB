import re
from flask import render_template, url_for, redirect, request
from flask import current_app as app
from flask_login import login_required

from app.models import Manufacturer, Reagent, MadeReagent, MadeReagentToComp
from app.printer import print_label
from app.route import current_user
from app.helper_functions import *


@app.route("/made_reagent/<int:made_reagent_id>", methods=["GET", "POST"])
@login_required
def made_reagent(made_reagent_id):
    made_reagent1 = MadeReagent.query.get(made_reagent_id)
    if not made_reagent1:
        return render_template('404.html'), 404

    # Make sure Reagent is deleted within 24 hours
    deletable = (datetime.now() - made_reagent1.date_entered).total_seconds() < 24 * 3600
    if request.method == 'POST':
        if "comment" in request.form:
            made_reagent1.comment = request.form.get("comment")
        elif "mr_id" in request.form:
            made_reagent1.name = re.sub(' +', ' ', request.form.get("name"))
            edit_values(made_reagent1, request)
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

        new_made_reagent = MadeReagent(
            name=re.sub(' +', ' ', request.form.get("name")),
            exp_date=exp_date,
            date_entered=datetime.now(),
            quantity=quantity,
            date_tested=date_tested,
            p_num=request.form.get('p_num'),
            comment=request.values.get("comment"),
            user_id=current_user.id
        )

        uids = []
        for value in range(new_made_reagent.quantity):
            uids.append(new_made_reagent.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(value + 1) + "/" + str(new_made_reagent.quantity))
            new_made_reagent.uids = ",".join(uids)
        db.session.add(new_made_reagent)
        db.session.commit()

        names = request.form.getlist("comp_name")
        comments = request.form.getlist("condition")
        is_first = True
        for name, comment in zip(names, comments):
            if is_first:
                is_first = False
                continue
            reagents = Reagent.query.filter_by(name=name)
            components = Component.query.filter_by(name=name)
            made_reagent_to_comp = None
            if reagents.count() > 0:
                made_reagent_to_comp = MadeReagentToComp(madereagent_id=new_made_reagent.id, reagent_id=reagents.first().id, comment=comment)
            elif components.count() > 0:
                made_reagent_to_comp = MadeReagentToComp(madereagent_id=new_made_reagent.id, comp_id=components.first().id,  comment=comment)

            if made_reagent_to_comp:
                db.session.add(made_reagent_to_comp)
                db.session.commit()
        db.session.commit()

        return redirect(url_for("made_reagent", made_reagent_id=new_made_reagent.id))

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
    made_reagent1 = MadeReagent.query.filter_by(id=made_reagent_id)[0]

    made_reagent_label_size = request.form.get('made_reagent_label_size')
    acquired_stat = request.form.get('acquired_stat')
    sm_printer_id = request.form.get('sm_printer_id')
    med_printer_id = request.form.get('med_printer_id')

    batch_num = 0
    while batch_num < made_reagent1.quantity:
        printcont = (made_reagent1.name, made_reagent1.exp_date, made_reagent1.date_entered, (sm_printer_id, med_printer_id))
        print_label(printcont, "made reagent", made_reagent_label_size, acquired_stat, made_reagent1.get_uids()[batch_num])
        batch_num += 1

    return redirect(url_for("made_reagent", made_reagent_id=made_reagent_id))
