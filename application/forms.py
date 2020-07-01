from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField

from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import Login
from wtforms.fields.html5 import DateField




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