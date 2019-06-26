from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo


class RequestForm(FlaskForm):
	searchbox = StringField('searchbox', id='autocomplete', validators=[InputRequired(), Length(min=0, max=255)])


class AddKitForm(FlaskForm):
	name = StringField('Kit Name', validators=[DataRequired(), Length(min=2, max=100)])
	box_lot_barcode = StringField('Box Lot Barcode', validators=[DataRequired(), Length(min=2, max=100)])