from flask import render_template, url_for, redirect, request
from flask_app import app, db, current_user
from flask_app.models import Kit, Manufacturer, Component
from datetime import datetime, timedelta
from flask_app.printer import print_label


@app.route("/kits", methods=['GET', 'POST'])
def kits():
    if not current_user.logged_in():
        return redirect(url_for('login'))

    all_kits = Kit.query.all()
    if request.method == 'POST':
        search = request.form.get('searchbox')
        query_kits = Kit.query.filter_by(name=search)
        if query_kits.count() == 0:
            if len(search.split()) >= 3:
                date_searched = datetime.strptime(search.split()[0], "%Y-%m-%d")  # 2019-10-08 14:39:42 1/2
                batch = search.split()[2].split("/")
                query_kits = Kit.query.filter(Kit.date_entered >= date_searched,
                                              Kit.date_entered <= date_searched + timedelta(days=1),
                                              Kit.quantity >= batch[0], Kit.quantity == batch[1])
            else:
                query_kits = Kit.query.filter_by(barcode=search) #123456782023-04

        return render_template("kit/kits.html", kits=query_kits, all_kits=all_kits)
    return render_template("kit/kits.html", kits=all_kits, all_kits=all_kits)


@app.route("/kit/<int:kit_id>", methods=['GET', 'POST'])
def kit(kit_id):
    if not current_user.logged_in():
        return redirect(url_for('login'))
    kit = Kit.query.get(kit_id)
    if request.method == 'POST':
        id = request.form.get("comp_id")
        component = Component.query.filter_by(id=id)[0]
        component.name = request.form.get("comp_name")
        component.barcode = request.form.get("comp_barcode")
        component.part_num = request.form.get("part_num")
        component.lot_num = request.form.get("lot_num")
        component.exp_date = datetime.strptime(request.form.get("exp_date"), "%Y-%m-%d")
        component.condition = request.form.get("comp_condition")
        db.session.commit()
        return redirect(url_for("kit", kit_id=kit_id))
    return render_template("kit/kit.html", kit=kit, Manufacturer=Manufacturer, range=range(kit.quantity))


@app.route("/kit_delete/<int:kit_id>")
def kit_delete(kit_id):
    if not current_user.logged_in():
        return redirect(url_for('login'))
    kit = Kit.query.get(kit_id)
    current_time = datetime.today()
    if (current_time - kit.date_entered).total_seconds() > 24 * 3600:
        return redirect(url_for('kit', kit_id=kit_id))
    db.session.delete(kit)
    db.session.commit()
    return redirect(url_for('kits'))


@app.route("/add_kit", methods=["GET", "POST"])
def add_kit():
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
        if exp_date == "":
            exp_date = None
        elif exp_date:
            exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
        quantity = int(request.form.get("quantity"))

        kit = Kit(
            name=request.form.get("name"),
            barcode=request.form.get("barcode"),
            part_num=part_num,
            lot_num=lot_num,
            date_entered=datetime.today(),
            exp_date=exp_date,
            quantity=quantity,
            comment=request.values.get("comment"),
            manufacturer_fk=request.values.get("manu_name").split(",")[-1]
        )

        db.session.add(kit)
        db.session.commit()

        names = request.form.getlist("comp_name")
        comp_nums = request.form.getlist("comp_barcode")
        comp_part_nums = request.form.getlist("comp_part_num")
        comp_lot_nums = request.form.getlist("comp_lot_num")
        comp_exp_dates = request.form.getlist("comp_exp_date")
        conditions = request.form.getlist("condition")
        for value in range(kit.quantity):
            index = 1
            for name, comp_num, part_num, lot_num, exp_date, condition in zip(names, comp_nums, comp_part_nums,
                                                                              comp_lot_nums, comp_exp_dates,
                                                                              conditions):
                if exp_date == "":
                    exp_date = kit.date_entered.replace(year=kit.date_entered.year + 10)
                elif exp_date:
                    exp_date = datetime.strptime(exp_date, "%Y-%m-%d")

                if lot_num == "":
                    lot_num = kit.date_entered.strftime("%Y-%m-%d")

                component = Component(
                    name=name,
                    uid=kit.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(index) + "/" + str(
                        len(names)) + " " + str(value + 1) + "/" + str(kit.quantity),
                    barcode=comp_num,
                    part_num=part_num,
                    lot_num=lot_num,
                    exp_date=exp_date,
                    condition=condition,
                    kit_fk=kit.id
                )
                db.session.add(component)
                db.session.commit()
                index += 1

        return redirect(url_for("kit", kit_id=kit.id))

    manu_name = Manufacturer.query.all()
    today = datetime.today().date()
    return render_template("kit/add_kit.html", title="Add", manu_name=manu_name, today=today)


@app.route("/print_kit/<int:kit_id>", methods=["GET", "POST"])
def print_kit(kit_id):
    kit = Kit.query.filter_by(id=kit_id)[0]

    kit_label_size = request.form.get('kit_label_size')
    kit_label = int(request.form.get('kit_label'))
    comp_label_s = int(request.form.get('comp_label_s'))
    comp_label_m = int(request.form.get('comp_label_m'))

    batchnum = 1
    batchpartnum = 1
    while batchnum <= kit_label:
        printcont = (kit.name, kit.exp_date, kit.date_entered)
        print_label(printcont, "kit", kit_label_size, None, str(batchpartnum) + '/' + str(kit.quantity))
        batchpartnum += 1
        if batchpartnum > kit.quantity:
            batchpartnum = 1
        batchnum += 1

    for component in kit.components:
        batchnum = 1
        batchpartnum = 1
        while batchnum <= comp_label_s:
            printcont = (component.name, component.exp_date, kit.date_entered)
            print_label(printcont, "kit", "s", None, str(batchpartnum) + '/' + str(comp_label_s))
            batchpartnum += 1
            if batchpartnum > kit.quantity:
                batchpartnum = 1
            batchnum += 1

        batchnum = 1
        batchpartnum = 1
        while batchnum <= comp_label_m:
            printcont = (component.name, component.exp_date, kit.date_entered)
            print_label(printcont, "kit", "m", None, str(batchpartnum) + '/' + str(comp_label_m))
            batchpartnum += 1
            if batchpartnum > kit.quantity:
                batchpartnum = 1
            batchnum += 1
    return redirect(url_for("kit", kit_id=kit_id))
