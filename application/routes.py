from application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for, session, jsonify
from flask_restplus import Resource
import mongoengine.errors
from application.forms import LoginForm, PatientForm
from application.models import Login, Patient

search_ssn = None

@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
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


@app.route("/create_patient", methods=["GET", "POST"])
def create_patient():
    if not session.get('username'):
        return redirect(url_for('login'))

    form = PatientForm()

    if form.validate_on_submit():
        patient_id = Patient.objects.count()
        patient_id += 1
        ssn_id = form.ssn_id.data
        name = form.patient_name.data
        age = int(form.patient_age.data)
        adm_date = form.admission_date.data
        bed_type = form.bed_type.data
        address = form.address.data
        city = form.city.data
        state = form.state.data

        try:
            if ssn_id:
                patient = Patient(patient_id=patient_id, ssn_id=ssn_id, name=name, age=age, admission=adm_date,
                              bed_type=bed_type, city=city, state=state, address=address)
                patient.save()
                flash("Patient Registered Successfully", 'success')
                return redirect(url_for("create_patient"))
            else:
                flash("Sorry, Something went Wrong", 'danger')
        except mongoengine.errors.NotUniqueError:
            flash("SSN_ID is Taken. Please Enter New SSN id")
    return render_template("create_patient.html", title="Patients", form=form)


@app.route('/update_patient', methods=['GET', 'POST'])
def update_patient():
    form = PatientForm()

    global search_ssn

    search_id = form.ssn_id.data
    if search_id:
        try:
            search = Patient.objects.get(ssn_id=search_id)
            search_ssn = search_id
            return render_template("update_patient.html", title="update patient", form=form, new_ssn_id=True,search=search)
        except Patient.DoesNotExist:
            flash('Patient Does Not Exist', 'danger')

    id = search_ssn
    name = request.form.get('patient_name')
    age = request.form.get('patient_age')
    adm_date = request.form.get("admission_date")
    bed_type = request.form.get('bed_type')
    address = request.form.get('address')
    city = request.form.get('address')
    state = request.form.get("state")

    if name:

        update_data = Patient.objects.get(ssn_id=id)
        update_data.update(name=name, age=age, admission=adm_date, bed_type=bed_type, address=address, city=city,
                               state=state)
        print(update_data)

        if update_data:
            search_ssn=None
            flash("Updated Successfully", "success")
            return redirect(url_for("update_patient"))
        else:
            flash("Sorry, Something Went Wrong", "danger")

    return render_template("update_patient.html", title="Update Patient", form=form, new_ssn_id=False)


@app.route("/delete_patient", methods=['GET',"POST"])
def delete_patient():

    global search_ssn

    form = PatientForm()

    search_id = form.ssn_id.data
    if search_id:
        try:
            search = Patient.objects.get(ssn_id=search_id)
            search_ssn = search_id
            return render_template("delete_patient.html", title="Delete Patient", form=form, new_ssn_id=True,
                                   search=search)
        except Patient.DoesNotExist:
            flash('Patient Does Not Exist', 'danger')

    id_ = search_ssn
    if search_ssn is not None:
        delete_data = Patient.objects.get(ssn_id=id_)
        delete_data.delete()
        search_ssn = None
        flash("Data Deleted successfully", "success")

    return render_template("delete_patient.html", title="DELETE PATIENT", form=form)