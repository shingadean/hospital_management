from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField

from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import Login
from wtforms.fields.html5 import DateField
from application.models import Medicine


med_data = Medicine.objects

med_name = [(i.med_name, i.med_name) for i in med_data]
med_id = [(str(i.med_id), i.med_id) for i in med_data]
med_rate = [(str(i.med_rate), i.med_rate) for i in med_data]
med_quant = [(str(i.quantity), i.quantity) for i in med_data]


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5, max=10)])
    submit = SubmitField("Login")

class PatientForm(FlaskForm):
    ssn_id = IntegerField("Patient SSN Id", validators=[DataRequired()])
    patient_name = StringField("Patient Name", validators=[DataRequired()])
    patient_age = SelectField("Patient Age", choices=[(str(age),age) for age in range(1,110)],coerce=int, validate_choice=False)
    admission_date = DateField("Date of Admission", format='%Y-%m-%d')
    bed_type = SelectField("Type of Bed", validators=[DataRequired()], choices=[('General Ward','General Ward'), ('Semi Sharing','Semi Sharing'), ('Single Room','Single Room')], coerce=str)
    address = StringField("Address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    submit = SubmitField("SUBMIT")

class MedForm(FlaskForm):

    med_name = SelectField("Medicine Name", validators=[DataRequired()], choices=med_name, coerce=str)
    take = IntegerField("Enter Quantity", validators=[DataRequired()])
    submit = SubmitField("SUBMIT")