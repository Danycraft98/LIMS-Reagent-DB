from flask import render_template, url_for, redirect, request
from flask_login import login_required, current_user

from app import app, db
from app.models import BarcodePattern, Manufacturer, MadeReagent
from datetime import datetime


@app.route("/manufacturer/<int:manufacturer_id>", methods=["GET", "POST"])
@login_required
def manufacturer(manufacturer_id):
    manufacturer1 = Manufacturer.query.get(manufacturer_id)

    # Make sure Reagent is deleted within 24 hours
    deletable = (datetime.now() - manufacturer1.date_entered).total_seconds() < 24 * 3600
    if request.method == 'POST' and deletable:
        for kit in manufacturer1.kits:
            db.session.delete(kit)

        for reagent in manufacturer1.reagents:
            db.session.delete(reagent)

        db.session.delete(manufacturer1)
        db.session.commit()
        return redirect(url_for('elements', element_type='manufacturer'))
    return render_template("manufacturer/manufacturer.html", manufacturer=manufacturer1, deletable=deletable)


@app.route("/add_manufacturer", methods=["GET", "POST"])
@login_required
def add_manufacturer():
    if request.method == "POST":
        # Request values from html inputs
        barcode = request.form.get('barcode')
        try:
            part_start = int(request.form.get("part_start"))
            part_end = len(request.form.get("part_num")) + part_start
        except ValueError:
            part_start = part_end = -1

        try:
            lot_start = int(request.form.get("lot_start"))
            lot_end = len(request.form.get("lot_num")) + lot_start
        except ValueError:
            lot_start = lot_end = -1

        barcode_pat = BarcodePattern(
            part_start=part_start,
            part_end=part_end,
            lot_start=lot_start,
            lot_end=lot_end
        )
        db.session.add(barcode_pat)
        db.session.commit()

        try:
            exp_date_start = int(request.form.get("exp_date_start"))
            exp_date_end = exp_date_start + 7
        except ValueError:
            exp_date_start = exp_date_end = -1

        comp_barcode = request.form.get('comp_barcode')
        try:
            comp_part_start = int(request.form.get("comp_part_start"))
            comp_part_end = len(request.form.get("comp_part_num")) + comp_part_start
        except ValueError:
            comp_part_start = comp_part_end = -1

        try:
            comp_lot_start = int(request.form.get("comp_lot_start"))
            comp_lot_end = len(request.form.get("comp_lot_num")) + comp_lot_start
        except ValueError:
            comp_lot_start = comp_lot_end = -1

        comp_barcode_pat = BarcodePattern(
            part_start=comp_part_start,
            part_end=comp_part_end,
            lot_start=comp_lot_start,
            lot_end=comp_lot_end
        )
        db.session.add(comp_barcode_pat)
        db.session.commit()

        new_manufacturer = Manufacturer(
            name=request.form.get("manu_name"),
            date_entered=datetime.now(),
            barcode=barcode,
            comp_barcode=comp_barcode,
            exp_date_start=exp_date_start,
            exp_date_end=exp_date_end,
            barcode_fk=barcode_pat.id,
            comp_barcode_fk=comp_barcode_pat.id,
            user_id=current_user.id
        )
        db.session.add(new_manufacturer)
        db.session.commit()
        return redirect(url_for("manufacturer", manufacturer_id=new_manufacturer.id))
    return render_template("manufacturer/add_manufacturer.html")
