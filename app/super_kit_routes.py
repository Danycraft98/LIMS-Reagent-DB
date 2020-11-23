import re
from datetime import datetime
from flask import render_template, url_for, redirect, request
from flask import current_app as app
from flask_login import login_required

from app import db
from app.helper_functions import add_component
from app.models import SuperKit, Kit, Manufacturer
from app.route import current_user


# Super Kit Route
@app.route("/super_kit/<int:super_kit_id>", methods=['GET', 'POST'])
@login_required
def super_kit(super_kit_id):
    super_kit1 = SuperKit.query.get(super_kit_id)
    return render_template("super_kit/super_kit.html", super_kit=super_kit1)


# Add Super Kit Route
@app.route("/add_super_kit", methods=["GET", "POST"])
@login_required
def add_super_kit():
    if request.method == "POST":
        form = request.form

        # Add Super Kit
        super_kit1 = SuperKit(
            name=re.sub(' +', ' ', form.get("sk_name")),
            part_num=form.get("sk_part_num"),
            comment=request.values.get("sk_comment"),
            quantity=int(form.get("sk_quantity"))
        )

        db.session.add(super_kit1)
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
                super_kit_id=super_kit1.id
            )
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
                for num in range(super_kit1.quantity):
                    uids.append(new_kit.date_entered.strftime("%Y-%m-%d %H:%M:%S ") + str(num + 1) + "/" + str(super_kit.quantity) + " " + str(value + 1) + "/" + str(new_kit.quantity))
                    add_component(value, new_kit, names, comp_nums, comp_part_nums, comp_lot_nums, comp_exp_dates, sizes, conditions, (num, super_kit.quantity))
            new_kit.uids = ",".join(uids)
            db.session.commit()
            i += 1
        return redirect(url_for("elements", element_types="super_kits"))

    super_kits = SuperKit.query.all()
    manufacturers = Manufacturer.query.all()
    kits = Kit.query.all()
    today = datetime.now().date()
    return render_template("super_kit/add_super_kit.html", add_comp=True, manufacturers=manufacturers, today=today, kits=kits, super_kits=super_kits, list=list)
