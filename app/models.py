from app import app
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __str__(self):
        return self.name


# -----------------------------------------------------------------------------------------------
class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_entered = db.Column(db.DateTime)
    barcode = db.Column(db.String(255))
    comp_barcode = db.Column(db.String(255))
    exp_date_start = db.Column(db.Integer)
    exp_date_end = db.Column(db.Integer)

    barcode_fk = db.Column(db.Integer, db.ForeignKey('barcode_pattern.id'), nullable=True)
    comp_barcode_fk = db.Column(db.Integer, db.ForeignKey('barcode_pattern.id'), nullable=True)
    kits = db.relationship('Kit', lazy=True)
    reagents = db.relationship('Reagent', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_barcode_pat(self):
        return BarcodePattern.query.get(self.barcode_fk)

    def get_part_num(self, barcode):
        barcode_pat = self.get_barcode_pat()
        return barcode[barcode_pat.part_start:barcode_pat.part_end]

    def get_lot_num(self, barcode):
        barcode_pat = self.get_barcode_pat()
        return barcode[barcode_pat.lot_start:barcode_pat.lot_end]

    def get_comp_barcode_pat(self):
        return BarcodePattern.query.get(self.comp_barcode_fk)

    def get_comp_part_num(self, barcode):
        comp_barcode_pat = self.get_comp_barcode_pat()
        return barcode[comp_barcode_pat.part_start:comp_barcode_pat.part_end]

    def get_comp_lot_num(self, barcode):
        comp_barcode_pat = self.get_comp_barcode_pat()
        return barcode[comp_barcode_pat.lot_start:comp_barcode_pat.lot_end]

    def get_user(self):
        return User.query.get(self.user_id)


class BarcodePattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_start = db.Column(db.Integer)
    part_end = db.Column(db.Integer)
    lot_start = db.Column(db.Integer)
    lot_end = db.Column(db.Integer)


# -------------------------------------------------------------
class Element(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    barcode = db.Column(db.String(255))
    part_num = db.Column(db.String(255))
    lot_num = db.Column(db.String(255))
    exp_date = db.Column(db.DateTime)
    date_entered = db.Column(db.DateTime)
    date_tested = db.Column(db.DateTime)
    p_num = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    comment = db.Column(db.String(255))


class SuperKit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    part_num = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    kit = db.relationship('Kit', uselist=False, backref='kit')


class Kit(Element):
    components = db.relationship('Component', lazy='dynamic')
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=True)
    super_kit_id = db.Column(db.Integer, db.ForeignKey('super_kit.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_super_kit(self):
        return SuperKit.query.get(self.super_kit_id)

    def get_manufacturer(self):
        return Manufacturer.query.get(self.manufacturer_id)

    def get_user(self):
        return User.query.get(self.user_id)


class Reagent(Element):
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_manufacturer(self):
        return Manufacturer.query.get(self.manufacturer_id)

    def get_user(self):
        return User.query.get(self.user_id)


class MadeReagent(Element):
    components = db.relationship('MadeReagentToComp', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # components = db.relationship('Component', lazy=True)
    # reagents = db.relationship('Reagent', lazy=True)

    def get_components(self):
        components = []
        for component in self.components:
            if component.comp_id:
                components.append(Component.query.get(component.comp_id))
        return components

    def get_reagents(self):
        reagents = []
        for component in self.components:
            if component.reagent_id:
                reagents.append(Reagent.query.get(component.reagent_id))
        return reagents


    def get_user(self):
        return User.query.get(self.user_id)


class MadeReagentToComp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    madereagent_id = db.Column(db.Integer, db.ForeignKey('made_reagent.id'), nullable=False)
    reagent_id = db.Column(db.Integer, db.ForeignKey('reagent.id'))
    comp_id = db.Column(db.Integer, db.ForeignKey('component.id'))


# -----------------------------------------------------------------------------------------------
class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    uid = db.Column(db.String(255), nullable=False)
    barcode = db.Column(db.String(255))
    part_num = db.Column(db.String(255))
    lot_num = db.Column(db.String(255))
    exp_date = db.Column(db.DateTime)
    condition = db.Column(db.String(255))
    size = db.Column(db.String(255), nullable=False)
    kit_id = db.Column(db.Integer, db.ForeignKey('kit.id'))


# -----------------------------------------------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    db.create_all()
