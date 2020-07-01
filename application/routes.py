from application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for, session, jsonify
from flask_restplus import Resource
from application.forms import LoginForm, PatientForm
from application.models import Login, Patient


@app.route("/login", methods=["GET","POST"])
@app.route("/", methods=["GET","POST"])
def login():
    if session.get('username'):
        return redirect(url_for('create_patient'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        login_form = Login.objects(username=username).first()
        if login_form and password:
            flash("You are Logged IN", 'success')
            session['username'] = login_form.username
            return redirect(url_for("create_patient"))
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
def logout():
    session['username'] = False
    flash("You are logged out", 'alert')
    return redirect(url_for('login'))


@app.route("/create_patient", methods=["GET","POST"])
def create_patient():
    form = PatientForm()

    if form.validate_on_submit():
        patient_id = Patient.objects.count()
        patient_id+=1
        ssn_id = form.ssn_id.data
        name = form.patient_name.data
        age = int(form.patient_age.data)
        adm_date = form.admission_date.data
        bed_type = form.bed_type.data
        address = form.address.data
        city = form.city.data
        state = form.state.data

        if ssn_id:
            patient = Patient(patient_id=patient_id, ssn_id=ssn_id, name=name, age=age, admission=adm_date, bed_type=bed_type, city=city, state=state, address=address)
            patient.save()
            flash("Patient Registered Successfully", 'success')
            return redirect(url_for("create_patient"))
        else:
            flash("Sorry, Something went Wrong", 'danger')

    return render_template("create_patient.html", title="Patients", form=form)


@app.route('/update_patient', methods=['GET','POST'])
def update_patient():

    form = PatientForm()

    new_ssn_id = form.ssn_id.data

    if new_ssn_id:

        search = list(Patient.objects.find(*[
            [
                {
                    '$match': {
                        'ssn_id': new_ssn_id
                    }
                }
            ]
        ]))

        if search:
            return "<h1>Heello</h1>"

    return render_template("update_patient.html", title="Update Patient",form=form)