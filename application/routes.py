from application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for, session, jsonify
from flask_restplus import Resource
from application.forms import LoginForm, PatientForm, MedForm
from application.models import Login, Patient, IssueMedicine, Medicine
import copy

search_ssn = None
med_name_search = None
med_id_search = None


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

        if ssn_id:
            patient = Patient(patient_id=patient_id, ssn_id=ssn_id, name=name, age=age, admission=adm_date,
                              bed_type=bed_type, city=city, state=state, address=address)
            patient.save()
            flash("Patient Registered Successfully", 'success')
            return redirect(url_for("create_patient"))
        else:
            flash("Sorry, Something went Wrong", 'danger')

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
            return render_template("update_patient.html", title="update patient", form=form, new_ssn_id=True,
                                   search=search)
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
            search_ssn = None
            flash("Updated Successfully", "success")
            return redirect(url_for("update_patient"))
        else:
            flash("Sorry, Something Went Wrong", "danger")

    return render_template("update_patient.html", title="Update Patient", form=form, new_ssn_id=False)


@app.route("/delete_patient", methods=['GET', "POST"])
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


@app.route("/pharmacy", methods=["GET", "POST"])
def pharmacy():
    global search_ssn

    form = PatientForm()

    search_id = form.ssn_id.data
    if search_id:
        try:
            search = Patient.objects.get(ssn_id=search_id)
            search_ssn = search_id
            med_details = IssueMedicine.objects.get(ssn_id=search_id)
            return render_template("pharmacy.html", title="Pharmacy Details", form=form, new_ssn_id=True,
                                   search=search, med=med_details)
        except Patient.DoesNotExist:
            flash('Patient Does Not Exist', 'danger')
        except IssueMedicine.DoesNotExist:
            return render_template("pharmacy.html", title="Pharmacy Details", form=form, new_ssn_id=True,
                                   search=search, med=None)

    return render_template("pharmacy.html", title="PHARMACY", form=form, new_ssn_id=False)


@app.route('/add_medicine/<id>', methods=["GET", "POST"])
def add_medicine(id):
    global search_ssn, med_id_search, med_name_search

    form = MedForm()

    name_med = form.med_name.data

    if name_med:
        med_details = Medicine.objects.get(med_name=name_med)
        search_ssn = id
        med_name_search = name_med
        med_id_search = med_details.med_id
        return render_template("add_medicine.html", title="Add Medicine", form=form, med_name=True,
                               search=med_details, patient_id=id)

    intake_quant = form.take.data
    if intake_quant is not None:
        Med_data = Medicine.objects.get(med_id=med_id_search)
        curr_quant = Med_data.quantity
        new = curr_quant - intake_quant

        check = list(IssueMedicine.objects.aggregate(*
                                                     [
                                                         {
                                                             '$match': {
                                                                 'ssn_id': search_ssn
                                                             }
                                                         }
                                                     ]
                                                     ))
        print(check)
        if len(check) == 0:

            new_issue = IssueMedicine(ssn_id = search_ssn, med_id= [med_id_search], med_name = [med_name_search], quantity_taken=[intake_quant])
            new_issue.save()
            Med_data.update(quantity = new)
            return "<h1>HII</h1>"
        else:

            update_issue = IssueMedicine.objects.get(ssn_id=search_ssn)
            update_issue.update(push__quantity_taken=intake_quant)

            return "<h1>123</h1>"



    return render_template("add_medicine.html", id=search_ssn, med_name=False, form=form, title="ADD MEDICINE")
