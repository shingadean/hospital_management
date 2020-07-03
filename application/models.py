import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
import email_validator


class Login(db.Document):
    username = db.StringField(maxlength=50, unique=True)
    password = db.StringField()

class Patient(db.Document):
    patient_id = db.IntField()
    ssn_id = db.IntField(unique=True)
    name = db.StringField()
    age=db.IntField()
    admission = db.DateField()
    bed_type = db.StringField()
    address = db.StringField()
    city = db.StringField()
    state = db.StringField()


class Medicine(db.Document):
    med_id = db.IntField(unique=True)
    med_name = db.StringField()
    quantity = db.IntField()
    med_rate = db.IntField()

class IssueMedicine(db.Document):

    ssn_id = db.IntField(unique=True,)
    med_id = db.ListField(default = [])
    med_name = db.ListField()
    quantity_taken = db.ListField()