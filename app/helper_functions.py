from datetime import datetime
import re

from app.models import db, Component


def edit_values(item, request):
    item.exp_date = datetime.strptime(request.form.get("exp_date"), "%Y-%m-%d")
    if request.form.get("date_tested"):
        item.date_tested = datetime.strptime(request.form.get("date_tested"), "%Y-%m-%d")
    item.p_num = request.form.get("p_num")
    item.quantity = int(request.form.get("quantity"))
    item.set_uids(item.quantity)


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
            component.uid = new_kit.date_entered.strftime("%Y-%m-%d %H:%M:%S") + " " + str(superk[0] + 1) + "/" + str(superk[1]) + " " + str(value + 1) + "/" + str(new_kit.quantity) + " " + str(index) + "/" + str(len(names) - 1)
        db.session.add(component)
        db.session.commit()
        index += 1
