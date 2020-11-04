import re
from datetime import datetime
from flask import render_template, url_for, redirect, request
from flask import current_app as app
from flask_login import login_required

from app import db
from app.models import SuperKit, Kit, Manufacturer, Component
from app.printer import print_label
from app.route import current_user


# Create component method
def add_component(value, new_kit, names, comp_nums, comp_part_nums, comp_lot_nums, comp_exp_dates, sizes, conditions, superk=None):
    index = 1
    for name, comp_num, part_num, lot_num, exp_date, size, condition in zip(names, comp_nums, comp_part_nums, comp_lot_nums, comp_exp_dates, sizes, conditions):
        if name == "":
            continue
        try:
            exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
        except ValueError:
            exp_date = new_kit.date_entered.replace(year=new_kit.date_entered.year + 10)

        if lot_num == "":
            lot_num = new_kit.date_entered.date()

        component = Component(
            name=re.sub(' +', ' ', name),
            uid=new_kit.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(value + 1) + "/" + str(new_kit.quantity) + " " + str(index) + "/" + str(len(names) - 1),
            barcode=comp_num,
            part_num=part_num,
            lot_num=lot_num,
            exp_date=exp_date,
            size=size,
            condition=condition,
            kit_id=new_kit.id
        )

        if superk:
            component.uid = new_kit.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(superk[0] + 1) + "/" + str(superk[1]) + " " + str(value + 1) + "/" + str(new_kit.quantity) + " " + str(index) + "/" + str(len(names) - 1),
        db.session.add(component)
        db.session.commit()
        index += 1


# Kit Route
@app.route("/kit/<int:kit_id>", methods=['GET', 'POST'])
@login_required
def kit(kit_id):
    kit1 = Kit.query.get(kit_id)
    for c in kit1.components.all():
        print(c.uid)
    if not kit1:
        return render_template('404.html'), 404

    super_kit = kit1.get_super_kit()
    # Make sure Kit is deleted within 24 hours
    deletable = (datetime.now() - kit1.date_entered).total_seconds() < 24 * 3600
    if request.method == 'POST':
        form_value = dict(request.form)
        if "kit_comment" in form_value or "super_comment" in form_value:
            kit1.comment = form_value.get("kit_comment")
            db.session.merge(kit1)
            if super_kit and "super_comment" in form_value:
                super_kit.comment = form_value.get("super_comment")
                db.session.merge(super_kit)
            db.session.commit()
        elif "comp_id" in form_value:
            comp_id = form_value.pop("comp_id")
            if comp_id == "0":
                sk_num = 1
                if kit1.get_super_kit():
                    sk_num = kit1.get_super_kit().quantity
                count = 1 + kit1.components.count() // kit1.quantity // sk_num
                for comp in kit1.components:
                    uid_parts = comp.uid.split("/")
                    uid_parts[-1] = str(count)
                    comp.uid = "/".join(uid_parts)
                for sk_id in range(sk_num):
                    for i in range(kit1.quantity):
                        if not form_value.get("exp_date"):
                            form_value["exp_date"] = kit1.date_entered.replace(year=kit1.date_entered.year + 10)
                        if sk_num < 2:
                            uid = kit1.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(i + 1) + "/" + str(kit1.quantity) + " " + str(count) + "/" + str(count)
                        else:
                            uid = kit1.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(sk_id + 1) + "/" + str(sk_num) + " " + str(i + 1) + "/" + str(kit1.quantity) + " " + str(count) + "/" + str(count)
                        new_comp = Component(**form_value, kit_id=kit1.id, uid=uid, size="s")
                        db.session.add(new_comp)
            else:
                Component.query.filter_by(id=comp_id).update(form_value)
            db.session.commit()
        elif "kit_id" in form_value:
            kit1.date_entered = datetime.now()
            kit1.name = re.sub(' +', ' ', form_value.get("name"))
            kit1.name = re.sub(' +', ' ', form_value.get("name"))
            kit1.barcode = form_value.get("barcode")
            kit1.part_num = form_value.get("part_num")
            kit1.lot_num = form_value.get("lot_num")
            kit1.exp_date = datetime.strptime(form_value.get("exp_date"), "%Y-%m-%d")
            if form_value.get("date_tested"):
                kit1.date_tested = datetime.strptime(form_value.get("date_tested"), "%Y-%m-%d")
            kit1.p_num = form_value.get("p_num")

            new_quantity = int(form_value.get("quantity"))
            sk_num = 1
            if kit1.get_super_kit():
                sk_num = kit1.get_super_kit().quantity
            count = kit1.components.count() // kit1.quantity // sk_num
            kit1.set_uids(new_quantity)
            if kit1.quantity > new_quantity:
                count2 = (kit1.quantity - new_quantity) * count * sk_num
                for i in range(count2):
                    db.session.delete(kit1.components[-1])
            elif kit1.quantity < new_quantity:
                for sk_id in range(sk_num):
                    for i in range(kit1.quantity, new_quantity):
                        j = 1
                        for c in kit1.components[:count]:
                            component = Component(
                                name=c.name,
                                uid=kit1.date_entered.strftime("%Y-%m-%d %H:%M:%S ") + str(i + 1) + "/" + str(new_quantity) + " " + str(j) + "/" + str(count),
                                barcode=c.barcode,
                                part_num=c.part_num,
                                lot_num=c.lot_num,
                                exp_date=c.exp_date,
                                size=c.size,
                                condition=c.condition,
                                kit_id=kit1.id
                            )
                            if sk_num > 1:
                                component.uid = kit1.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(sk_id + 1) + "/" + str(sk_num) + " " + str(i + 1) + "/" + str(new_quantity) + " " + str(j) + "/" + str(count)
                            db.session.add(component)
                            j += 1
            for c in kit1.components:
                c.uid = kit1.date_entered.strftime("%Y-%m-%d %H:%M:%S") + re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}((?: \d+/\d+)? \d+)/\d+ (\d+/\d+)", "\\1/" + str(new_quantity) + " \\2", c.uid)
            kit1.quantity = new_quantity

            db.session.merge(kit1)
            db.session.commit()

    kit1 = Kit.query.get(kit_id)
    super_kit = kit1.get_super_kit()
    return render_template("kit/kit.html", kit=kit1, super_kit=super_kit, deletable=deletable)


# Add Super Kit Route
@app.route("/add_kit", methods=["GET", "POST"])
@login_required
def add_kit():
    if request.method == "POST":
        form = request.form
        super_kit = None
        if form.get("sk_name"):
            sk_name = re.sub(' +', ' ', form.get("sk_name"))

            # Add Super Kit
            super_kit = SuperKit(
                name=sk_name,
                part_num=form.get("sk_part_num"),
                comment=request.values.get("sk_comment"),
                quantity=int(form.get("sk_quantity"))
            )

            db.session.add(super_kit)
            db.session.commit()

        ids = form.get("kit_ids").split(",")
        for kit_id in ids:
            i = int(kit_id)
            try:
                exp_date = datetime.strptime(form.get("k" + str(i) + "_exp_date"), "%Y-%m-%d")
            except ValueError:
                exp_date = None

            try:
                date_tested = datetime.strptime(form.get("k" + str(i) + "_date_tested"), "%Y-%m-%d")
            except ValueError:
                date_tested = None

            try:
                manufacturer_id = int(form.get("k" + str(i) + "_manu_name").split(",")[0])
                if manufacturer_id == 0:
                    manufacturer_id = None
            except ValueError:
                manufacturer_id = None

            new_kit = Kit(
                name=re.sub(' +', ' ', form.get("k" + str(i) + "_name")),
                manufacturer_id=manufacturer_id,
                barcode=form.get("k" + str(i) + "_barcode"),
                part_num=form.get("k" + str(i) + "_part_num"),
                lot_num=form.get("k" + str(i) + "_lot_num"),
                exp_date=exp_date,
                date_entered=datetime.now(),
                date_tested=date_tested,
                p_num=form.get("k" + str(i) + "_p_num"),
                quantity=int(form.get("k" + str(i) + "_quantity", 1)),
                comment=form.get("k" + str(i) + "_value"),
                user_id=current_user.id,
            )

            if super_kit:
                new_kit.super_kit_id = super_kit.id

            db.session.add(new_kit)
            db.session.commit()

            names = form.getlist("k" + str(i) + "_comp_name")
            comp_nums = form.getlist("k" + str(i) + "_comp_barcode")
            comp_part_nums = form.getlist("k" + str(i) + "_comp_part_num")
            comp_lot_nums = form.getlist("k" + str(i) + "_comp_lot_num")
            comp_exp_dates = form.getlist("k" + str(i) + "_comp_exp_date")
            sizes = form.getlist("k" + str(i) + "_size")
            conditions = form.getlist("k" + str(i) + "_condition")

            uids = []
            for value in range(new_kit.quantity):
                if super_kit:
                    for num in range(super_kit.quantity):
                        uids.append(new_kit.date_entered.strftime("%Y-%m-%d %H:%M:%S ") + str(num + 1) + "/" + str(super_kit.quantity) + " " + str(value + 1) + "/" + str(new_kit.quantity))
                        add_component(value, new_kit,names, comp_nums, comp_part_nums, comp_lot_nums, comp_exp_dates, sizes, conditions, (num, super_kit.quantity))
                else:
                    uids.append(new_kit.date_entered.strftime("%Y-%m-%d %H:%M:%S ")+ str(value + 1) + "/" + str(new_kit.quantity))
                    add_component(value, new_kit, names, comp_nums, comp_part_nums, comp_lot_nums, comp_exp_dates, sizes, conditions)
            new_kit.uids = ",".join(uids)
            print(uids)
            db.session.commit()
            i += 1
        return redirect(url_for("elements", element_types="kits"))

    super_kits = SuperKit.query.all()
    manufacturers = Manufacturer.query.all()
    kits = Kit.query.all()
    today = datetime.now().date()
    return render_template("kit/add_kit.html", add_comp=True, manufacturers=manufacturers, today=today, kits=kits, super_kits=super_kits, list=list)


# Print Kit Route
@app.route("/print_kit/<int:kit_id>", methods=["GET", "POST"])
@login_required
def print_kit(kit_id):
    kit1 = Kit.query.filter_by(id=kit_id)[0]
    comp_print = request.form.get('comp_print')
    kit_label_size = request.form.get('kit_label_size')
    printer_id = request.form.get('printer_id')

    if not comp_print:
        batch_num = 1
        while batch_num <= kit1.quantity:
            print_cont = (kit1.name, kit1.exp_date, kit1.date_entered, printer_id)
            print_label(print_cont, "kit", kit_label_size, None, kit1.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(batch_num) + '/' + str(kit1.quantity))
            batch_num += 1

        for component in kit1.components:
            print_cont = (component.name, component.exp_date, kit1.date_entered, printer_id)
            print_label(print_cont, "kit", component.size, None, component.uid)
    else:
        component = Component.query.filter_by(id=comp_print)[0]
        print_cont = (component.name, component.exp_date, kit1.date_entered, printer_id)
        print_label(print_cont, "kit", component.size, None, component.uid)

    return redirect(url_for("kit", kit_id=kit_id))
