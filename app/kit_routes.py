from flask import render_template, url_for, redirect, request
from flask_login import login_required
from datetime import datetime

from app import app, db
from app.models import SuperKit, Kit, Manufacturer, Component
from app.printer import print_label
from app.route import current_user


# Kit Route
@app.route("/kit/<int:kit_id>", methods=['GET', 'POST'])
@login_required
def kit(kit_id):
    kit1 = Kit.query.get(kit_id)
    if not kit1:
        return render_template('404.html'), 404

    super_kit = kit1.get_super_kit()
    # Make sure Kit is deleted within 24 hours
    deletable = (datetime.now() - kit1.date_entered).total_seconds() < 24 * 3600
    if request.method == 'POST':
        if "kit_comment" in request.form or "super_comment" in request.form:
            kit1.comment = request.form.get("kit_comment")
            db.session.merge(kit1)
            if super_kit and "super_comment" in request.form:
                super_kit.comment = request.form.get("super_comment")
                db.session.merge(super_kit)
            db.session.commit()
        elif "comp_id" in request.form:
            comp = Component.query.get(request.form.get('comp_id'))
            comp.name = request.form.get("name")
            comp.barcode = request.form.get("barcode")
            comp.part_num = request.form.get("part_num")
            comp.lot_num = request.form.get("lot_num")
            comp.exp_date = datetime.strptime(request.form.get("exp_date"), "%Y-%m-%d")
            comp.condition = request.form.get("condition")
            db.session.merge(comp)
            db.session.commit()

    kit1 = Kit.query.get(kit_id)
    super_kit = kit1.get_super_kit()
    return render_template("kit/kit.html", kit=kit1, manufacturer=kit1.get_manufacturer(), super_kit=super_kit, range=range(kit1.quantity), deletable=deletable)


# Add Kit Route
@app.route("/add_kit", methods=["GET", "POST"])
@login_required
def add_kit():
    if request.method == "POST":
        form = request.form
        sk_name = form.get('sk_name')

        # Add Super Kit
        super_kit = None
        if sk_name != '':
            super_kit = SuperKit(
                name=sk_name,
                part_num=form.get("sk_part_num"),
                comment=request.values.get("sk_comment")
            )

            db.session.add(super_kit)
            db.session.commit()

        try:
            exp_date = datetime.strptime(form.get("exp_date"), "%Y-%m-%d")
        except ValueError:
            exp_date = None

        try:
            date_tested = datetime.strptime(form.get("date_tested"), "%Y-%m-%d")
        except ValueError:
            date_tested = None

        try:
            manufacturer_id = int(request.values.get("manu_name").split(",")[0])
            if manufacturer_id == 0:
                manufacturer_id = None
        except ValueError:
            manufacturer_id = None

        new_kit = Kit(
            name=form.get("name"),
            manufacturer_id=manufacturer_id,
            barcode=form.get("barcode"),
            part_num=form.get("part_num"),
            lot_num=form.get("lot_num"),
            exp_date=exp_date,
            date_entered=datetime.now(),
            date_tested=date_tested,
            p_num=form.get("p_num"),
            quantity=int(form.get("quantity", "1")),
            comment=request.values.get("comment"),
            user_id=current_user.id
        )

        if super_kit:
            new_kit.super_kit_id = super_kit.id

        db.session.add(new_kit)
        db.session.commit()

        names = form.getlist("comp_name")
        comp_nums = form.getlist("comp_barcode")
        comp_part_nums = form.getlist("comp_part_num")
        comp_lot_nums = form.getlist("comp_lot_num")
        comp_exp_dates = form.getlist("comp_exp_date")
        sizes = form.getlist("size")
        conditions = form.getlist("condition")

        for value in range(new_kit.quantity):
            is_first = True
            index = 1
            for name, comp_num, part_num, lot_num, exp_date, size, condition in zip(names, comp_nums, comp_part_nums, comp_lot_nums, comp_exp_dates, sizes, conditions):
                if is_first:
                    is_first = False
                    continue

                try:
                    exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
                except ValueError:
                    exp_date = new_kit.date_entered.replace(year=new_kit.date_entered.year + 10)

                if lot_num == "":
                    lot_num = new_kit.date_entered.date()

                component = Component(
                    name=name,
                    uid=new_kit.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(value + 1) + "/" + str(new_kit.quantity) + " " + str(index) + "/" + str(len(names)-1),
                    barcode=comp_num,
                    part_num=part_num,
                    lot_num=lot_num,
                    exp_date=exp_date,
                    size=size,
                    condition=condition,
                    kit_id=new_kit.id
                )
                db.session.add(component)
                db.session.commit()
                index += 1

        return redirect(url_for("kit", kit_id=new_kit.id))

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

    if not comp_print:
        batch_num = 1
        while batch_num <= kit1.quantity:
            print_cont = (kit1.name, kit1.exp_date, kit1.date_entered)
            print_label(print_cont, "kit", kit_label_size, None, kit1.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(batch_num) + '/' + str(kit1.quantity))
            batch_num += 1

        for component in kit1.components:
            print_cont = (component.name, component.exp_date, kit1.date_entered)
            print_label(print_cont, "kit", component.size, None, component.uid)
    else:
        component = Component.query.filter_by(id=comp_print)[0]
        print_cont = (component.name, component.exp_date, kit1.date_entered)
        print_label(print_cont, "kit", component.size, None, component.uid)

    return redirect(url_for("kit", kit_id=kit_id))
