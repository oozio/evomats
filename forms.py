from wtforms.validators import InputRequired
from wtforms import TextField, IntegerField, Form

class idForm(Form):
	mons_id = IntegerField(u'monster ID',[InputRequired()])