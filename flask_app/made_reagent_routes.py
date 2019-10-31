from flask import render_template, url_for, redirect, request
from flask_app import app, db, current_user
from flask_app.models import Manufacturer, Reagent, MadeReagent, Component
from flask_app.printer import print_label

from collections import Counter
from datetime import datetime, timedelta


@app.route("/made_reagents", methods=['GET', 'POST'])
def made_reagents():
    if not current_user.logged_in():
        return redirect(url_for('login'))
    all_made_reagents = MadeReagent.query.all()
    if request.method == 'POST':
        search = request.form.get('searchbox')
        query_m_reagents = MadeReagent.query.filter_by(name=search)
        if query_m_reagents.count() == 0:
            if len(search.split()) >= 3:
                date_searched = datetime.strptime(search.split()[0], "%Y-%m-%d")  # 2019-10-08 14:39:42 1/2
                batch = search.split()[2].split("/")
                query_m_reagents = MadeReagent.query.filter(MadeReagent.date_entered >= date_searched, MadeReagent.date_entered <= date_searched + timedelta(days=1), MadeReagent.quantity >= batch[0], MadeReagent.quantity == batch[1])
            else:
                query_m_reagents = MadeReagent.query.filter_by(barcode=search)  # 123456782023-04
                if query_m_reagents.count() == 0:
                    if "-" in search:
                        date_searched = datetime.strptime(search, "%Y-%m-%d")  # 2019-10-08
                        query_m_reagents = MadeReagent.query.filter(MadeReagent.date_entered >= date_searched, MadeReagent.date_entered <= date_searched + timedelta(days=1))

        return render_template("made_reagent/made_reagents.html", made_reagents=query_m_reagents, all_made_reagents=all_made_reagents)
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

    if request.method == "POST":
        exp_date = request.form.get("exp_date")
        if exp_date == '':
            exp_date = None
        elif exp_date:
            exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
        quantity = int(request.form.get("quantity"))

        made_reagent = MadeReagent(
            name=request.form.get("name"),
            exp_date=exp_date,
            date_entered=datetime.today(),
            quantity=quantity
        )

        db.session.add(made_reagent)
        db.session.commit()

        names = Counter(request.form.getlist("comp_name"))
        reagent_list = {}
        component_list = {}
        for name in names:
            if len(list(Reagent.query.filter_by(name=name))) > 0:
                reagent_list[name] = names[name]
            elif len(list(Component.query.filter_by(name=name))) > 0:
                component_list[name] = names[name]
        made_reagent.reagent_list = str(reagent_list)
        made_reagent.component_list = str(component_list)
        db.session.commit()

        return redirect(url_for("made_reagent", made_reagent_id=made_reagent.id))

    comp_infos = {}
    for comp in Component.query.all():
        comp_infos[comp.barcode] = comp.name

    for reagent in Reagent.query.all():
        comp_infos[reagent.barcode] = reagent.name
    today = datetime.today().date()
    return render_template("made_reagent/add_made_reagent.html", today=today, comp_infos=comp_infos)


@app.route("/print_made_reagent/<int:made_reagent_id>", methods=["GET", "POST"])
def print_made_reagent(made_reagent_id):
    made_reagent = MadeReagent.query.filter_by(id=made_reagent_id)

    made_reagent_label_size = request.form.get('made_reagent_label_size')
    made_reagent_label = int(request.form.get('made_reagent_label'))
    comp_label_s = int(request.form.get('comp_label_s'))
    comp_label_m = int(request.form.get('comp_label_m'))
    acquired_stat = request.form.get('acquired_stat')

    batchnum = 1
    batchpartnum = 1
    while batchnum <= made_reagent.quantity:
        printcont = (made_reagent.name, made_reagent.exp_date, datetime.now())
        print_label(printcont, "made reagent", made_reagent_label_size, acquired_stat, str(batchnum) + '/' + str(made_reagent.quantity))
        batchpartnum += 1
        if batchpartnum > made_reagent.quantity:
            batchpartnum = 1
        batchnum += 1

    for component in made_reagent.component_list:
        batchnum = 1
        batchpartnum = 1
        while batchnum <= comp_label_s:
            printcont = (component.name, component.exp_date, datetime.now())
            print_label(printcont, "made reagent", "s", acquired_stat, str(batchpartnum) + '/' + str(made_reagent.quantity))
            batchpartnum += 1
            if batchpartnum > made_reagent.quantity:
                batchpartnum = 1
            batchnum += 1

    for reagent in made_reagent.reagent_list:
        batchnum = 1
        batchpartnum = 1
        while batchnum <= comp_label_m:
            printcont = (reagent.name, reagent.exp_date, datetime.now())
            print_label(printcont, "made reagent", "m", acquired_stat, str(batchpartnum) + '/' + str(made_reagent.quantity))
            batchpartnum += 1
            if batchpartnum > made_reagent.quantity:
                batchpartnum = 1
            batchnum += 1

    return redirect(url_for("made_reagent", made_reagent_id=made_reagent_id))
