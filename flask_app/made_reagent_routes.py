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
            elif "-" in search:
                date_searched = datetime.strptime(search, "%Y-%m-%d")  # 2019-10-08
                query_m_reagents = MadeReagent.query.filter(MadeReagent.date_entered >= date_searched, MadeReagent.date_entered <= date_searched + timedelta(days=1))
                if query_m_reagents.count() == 0:
                    query_m_reagents = MadeReagent.query.filter(MadeReagent.component_list.contains(search))
                    if query_m_reagents.count() == 0:
                        query_m_reagents = MadeReagent.query.filter(MadeReagent.reagent_list.contains(search))
            else:
                query_component = Component.query.filter_by(barcode=search)
                query_reagent = Reagent.query.filter_by(barcode=search)
                query_m_reagents = []
                if query_component.count() > 0:
                    for comp in query_component:
                        query_m_reagents.extend(MadeReagent.query.filter(MadeReagent.component_list.contains(comp.name)))
                elif query_reagent.count() > 0:
                    for reagent in query_reagent:
                        query_m_reagents.extend(MadeReagent.query.filter(MadeReagent.reagent_list.contains(reagent.name)))

        return render_template("made_reagent/made_reagents.html", made_reagents= list(set(query_m_reagents)), all_made_reagents=all_made_reagents, username=current_user.get_name())
    return render_template("made_reagent/made_reagents.html", made_reagents=all_made_reagents, all_made_reagents=all_made_reagents, username=current_user.get_name())


@app.route("/made_reagent/<int:made_reagent_id>", methods=["GET", "POST"])
def made_reagent(made_reagent_id):
    if not current_user.logged_in():
        return redirect(url_for('login'))
    made_reagent = MadeReagent.query.get(made_reagent_id)

    # Make sure Reagent is deleted within 24 hours
    deletable = (datetime.today() - made_reagent.date_entered).total_seconds() < 24 * 3600
    comment = request.form.get("comment")
    if request.method == 'POST':
        if comment:
            made_reagent.comment = comment
            db.session.commit()
            return redirect(url_for("made_reagent", made_reagent_id=made_reagent_id, username=current_user.get_name()))
        elif deletable:
            db.session.delete(made_reagent)
            db.session.commit()
            return redirect(url_for('made_reagents', username=current_user.get_name()))
    return render_template("made_reagent/made_reagent.html", made_reagent=made_reagent, eval=eval, Manufacturer=Manufacturer, Reagent=Reagent, Component=Component, deletable=deletable, username=current_user.get_name())


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

        made_reagent_ = MadeReagent(
            name=request.form.get("name"),
            exp_date=exp_date,
            date_entered=datetime.today(),
            quantity=quantity,
            comment=request.values.get("comment")
        )

        db.session.add(made_reagent_)
        db.session.commit()

        names = Counter(request.form.getlist("comp_name"))
        reagent_list = {}
        component_list = {}
        for name in names:
            if len(list(Reagent.query.filter_by(name=name))) > 0:
                reagent_list[name] = names[name]
            elif len(list(Component.query.filter_by(name=name))) > 0:
                component_list[name] = names[name]
        made_reagent_.reagent_list = str(reagent_list)
        made_reagent_.component_list = str(component_list)
        db.session.commit()

        return redirect(url_for("made_reagent", made_reagent_id=made_reagent_.id, username=current_user.get_name()))

    comp_infos = {}
    for comp in Component.query.all():
        comp_infos[comp.barcode] = comp.name

    for reagent in Reagent.query.all():
        comp_infos[reagent.barcode] = reagent.name
    today = datetime.today().date()
    return render_template("made_reagent/add_made_reagent.html", today=today, comp_infos=comp_infos, username=current_user.get_name())


@app.route("/print_made_reagent/<int:made_reagent_id>", methods=["GET", "POST"])
def print_made_reagent(made_reagent_id):
    made_reagent_ = MadeReagent.query.filter_by(id=made_reagent_id)[0]

    made_reagent_label_size = request.form.get('made_reagent_label_size')
    acquired_stat = request.form.get('acquired_stat')

    batchnum = 1
    while batchnum <= made_reagent_.quantity:
        printcont = (made_reagent_.name, made_reagent_.exp_date, made_reagent_.date_entered)
        print_label(printcont, "made reagent", made_reagent_label_size, acquired_stat, made_reagent_.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(batchnum) + '/' + str(made_reagent_.quantity))
        batchnum += 1

    return redirect(url_for("made_reagent", made_reagent_id=made_reagent_id, username=current_user.get_name()))
