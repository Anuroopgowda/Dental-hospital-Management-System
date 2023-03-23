from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import yaml
from tkinter import *
import sys

from yaml import load


app = Flask(__name__)

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


app.secret_key = "super secret key"
mysql = MySQL(app)

@app.route('/')
def front():
    return render_template('front.html')

@app.route('/front1')
def front1():
    return render_template('front1.html', email=session['email'])

@app.route('/front2')
def front2():
    return render_template('front2.html', doctor_id=session['doctor_id'])

@app.route('/front3')
def front3():
    return render_template('front3.html', admin_id=session['admin_id'])


@app.route('/doctor', methods=['GET','POST'])
def doctor():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        doctor_id = userDetails['doctor_id']
        doctor_name = userDetails['doctor_name']
        d_phone_number = userDetails['d_phone_number']
        doctor_dept_id = userDetails['doctors_dept_id']
        doctor_mail = userDetails['doctor_mail']
        yoe = userDetails['yoe']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO doctors(doctor_id, doctor_name, d_phone_number, doctors_dept_id, doctor_mail, yoe, password) VALUES(%s, %s, %s, %s, %s, %s, %s)', (doctor_id, doctor_name, d_phone_number, doctor_dept_id, doctor_mail, yoe, password))
        mysql.connection.commit()
        cur.close()
    return render_template('doctor.html')

@app.route('/patient', methods=['GET','POST'])
def patient():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        #patient_id = userDetails['patient_id']
        first_name = userDetails['first_name']
        last_name = userDetails['last_name']
        email = userDetails['email']
        gender = userDetails['gender']
        phone_number = userDetails['phone_number']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO patient(first_name, last_name, email, gender, phone_number, password) VALUES(%s, %s, %s, %s, %s, %s)', (first_name, last_name, email, gender, phone_number, password))
        mysql.connection.commit()
        cur.close()
    return render_template('patient.html')

@app.route('/enter_trans', methods=['GET','POST'])
def enter_trans():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        #transaction_id = userDetails['transaction_id']
        patients_id = userDetails['patients_id']
        amount = userDetails['amount']
        time = userDetails['time']
        date = userDetails['date']
        status = userDetails['status']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO enter_trans(patients_id, amount, time, date, status) VALUES(%s, %s, %s, %s, %s)', (patients_id, amount, time, date, status))
        mysql.connection.commit()
        cur.close()
    return render_template('enter_trans.html')

@app.route('/booking', methods=['GET','POST'])
def booking():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        #booking_id = userDetails['booking_id']
        patient_id = userDetails['patient_id']
        slot = userDetails['slot']
        date = userDetails['date']
        disease = userDetails['disease']
        dept_id = userDetails['dept_id']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO booking(patient_id, slot, date, disease, dept_id) VALUES(%s, %s, %s, %s, %s)', (patient_id, slot, date, disease, dept_id))
        mysql.connection.commit()
        cur.close()
    return render_template('booking.html')
#for patient
@app.route('/booking_details', methods=['GET', 'POST'])
def booking_details():
    patient_id = session['email']
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM booking WHERE patient_id = %s', (patient_id,))
    person = cur.fetchall()
    cur.close()
    return render_template('booking_details.html', person=person)



#for admin
@app.route('/booking_detailsA', methods=['GET', 'POST'])
def booking_detailsA():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `booking`")
    person = cur.fetchall()
    cur.close()
    return render_template('booking_detailsA.html', person=person)

#for doctor
# @app.route('/booking_detailsD', methods=['GET', 'POST'])
# def booking_detailsD():
#     doctor_id = session['doctor_id']
#     cur = mysql.connection.cursor()
#     cur.execute('SELECT * FROM booking WHERE dept_id = %s', (doctor_id,))
#     result = cur.fetchall()
#     cur.close()
#     return render_template('booking_detailsD.html', result=result)


@app.route('/booking_detailsD', methods=['GET', 'POST'])
def booking_detailsD():
    msg = ''
    if request.method == 'POST':
        dept_id = request.form['dept_id']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM booking WHERE dept_id = % s ', (dept_id,))
        account = cur.fetchone()
        if account:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM booking WHERE dept_id = % s ', (dept_id,))
            person = cur.fetchall()
            return render_template('booking_detailsD.html', person=person)
        else:
            msg = 'Incorrect patient id!'
        cur.close()
    return render_template('booking_detailsD.html', msg=msg)



@app.route('/show_trans', methods=['GET', 'POST'])
def show_trans():
    msg = ''
    if request.method == 'POST':
        patients_id = request.form['patients_id']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM enter_trans WHERE patients_id = % s ', (patients_id,))
        account = cur.fetchone()
        if account:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM enter_trans e,patient p WHERE e.patients_id=p.patient_id AND p.patient_id = % s ", (patients_id,))
            result = cur.fetchall()
            return render_template('show_trans.html', result=result)
        else:
            msg = 'Incorrect patient id!'
        cur.close()
    return render_template('show_trans.html', msg=msg)


@app.route('/show_transA', methods=['GET', 'POST'])
def show_transA():
    msg = ''
    if request.method == 'POST':
        patients_id = request.form['patients_id']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM enter_trans WHERE patients_id = % s ', (patients_id,))
        account = cur.fetchone()
        if account:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM enter_trans e,patient p WHERE e.patients_id=p.patient_id AND p.patient_id = % s ", (patients_id,))
            result = cur.fetchall()
            return render_template('show_transA.html', result=result)
        else:
            msg = 'Incorrect patient id!'
        cur.close()
    return render_template('show_transA.html', msg=msg)


@app.route('/mat', methods=['GET', 'POST'])
def mat():
    msg = ''
    if request.method == 'POST':
        patients_id = request.form['patients_id']
        transaction_id = request.form['transaction_id']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM enter_trans WHERE patients_id = % s AND transaction_id = %s', (patients_id, transaction_id,))
        account = cur.fetchone()
        if account:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM enter_trans e,patient p WHERE e.patients_id=p.patient_id AND p.patient_id = % s AND e.transaction_id = % s", (patients_id, transaction_id,))
            Result = cur.fetchall()
            return render_template('mat.html', Result=Result)
        else:
            msg = 'Incorrect patient id!'
        cur.close()
    return render_template('mat.html', msg=msg)

@app.route('/department', methods=['GET', 'POST'])
def department():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `department`")
    Result = cur.fetchall()
    return render_template('department.html', Result=Result)

@app.route('/all', methods=['GET', 'POST'])
def all():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `enter_trans` JOIN `patient`")
    result = cur.fetchall()
    return render_template('all.html', result=result)

@app.route('/patient_list', methods=['GET', 'POST'])
def patient_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `patient`")
    Result = cur.fetchall()
    return render_template('patient_list.html', Result=Result)

@app.route('/doctor_list', methods=['GET', 'POST'])
def doctor_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `doctors`")
    Result = cur.fetchall()
    return render_template('doctor_list.html', Result=Result)


@app.route('/Dlogin', methods=['GET','POST'])
def Dlogin():
    msg = ''
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM doctors WHERE doctor_id = % s AND password = % s', (doctor_id, password,))
        account = cur.fetchone()
        if account:
            popupwindow = Tk()
            popupwindow.title("alert")
            popupwindow.geometry("200x200")
            alert = Label(popupwindow, text="LOGGED IN SUCCESSFULLY")
            alert.pack()
            popupwindow.mainloop()
            session['logged'] = True
            session['doctor_id'] = account[3]
            return redirect(url_for('front2'))

        else:
            msg = 'Incorrect doctor id / password !'
        cur.close()
    return render_template('Dlogin.html', msg=msg)


@app.route('/Alogin', methods=['GET','POST'])
def Alogin():
    msg = ''
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE admin_id = % s AND password = % s', (admin_id, password,))
        account = cur.fetchone()
        if account:
            popupwindow = Tk()
            popupwindow.title("alert")
            popupwindow.geometry("200x200")
            alert = Label(popupwindow, text="LOGGED IN SUCCESSFULLY")
            alert.pack()
            popupwindow.mainloop()
            session['logged'] = True
            session['admin_id'] = account[1]
            return redirect(url_for('front3'))
        else:
            msg = 'Incorrect doctor id / password !'
    return render_template('Alogin.html', msg=msg)



@app.route('/Plogin', methods =['GET', 'POST'])
def Plogin():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM patient WHERE email = % s AND password = % s', (email, password, ))
        account = cur.fetchone()
        if account:
            popupwindow = Tk()
            popupwindow.title("alert")
            popupwindow.geometry("200x200")
            alert = Label(popupwindow, text="LOGGED IN SUCCESSFULLY")
            alert.pack()
            popupwindow.mainloop()
            session['logged'] = True
            session['email'] = account[0]

            return redirect(url_for('front1'))
        else:
            msg = 'Incorrect username / password !'
        cur.close()
    return render_template('Plogin.html', msg=msg)

@app.route('/logoutD')
def logoutD():
    session.pop('logged', None)
    session.pop('doctor_id', None)
    return redirect(url_for('front'))

@app.route('/logoutP')
def logoutP():
    session.pop('logged', None)
    session.pop('email', None)
    return redirect(url_for('front'))

@app.route('/logoutA')
def logoutA():
    session.pop('logged', None)
    session.pop('email', None)
    return redirect(url_for('front'))

# @app.route('/editB',methods=['POST','GET'])
# def editB():
#     if request.method == 'POST':
#         # Fetch form data
#         userDetails = request.form
#         booking_id = userDetails['booking_id']
#         patient_id = userDetails['patient_id']
#         slot = userDetails['slot']
#         date = userDetails['date']
#         disease = userDetails['disease']
#         dept_id = userDetails['dept_id']
#         cur = mysql.connection.cursor()
#         cur.execute("""
#         UPDATE booking
#         SET patient_id=%s, slot=%s, date=%s, disease=%s, dept_id=%s
#         WHERE booking_id=%s
#         """, (patient_id, slot, date, disease, dept_id, booking_id))
#         flash("Data Updated Successfully")
#         mysql.connection.commit()
#         cur.close()
#     return redirect(url_for('booking_details'))
#
# @app.route('/editB', methods=['GET', 'POST'])
# def editB():
#     msg = ''
#     if request.method == 'POST':
#         patients_id = request.form['patients_id']
#         booking_id = request.form['booking_id']
#         cur = mysql.connection.cursor()
#         cur.execute('SELECT * FROM booking WHERE patients_id = % s AND booking_id = %s', (patients_id, booking_id,))
#         account = cur.fetchone()
#         if account:
#             cur = mysql.connection.cursor()
#             cur.execute('SELECT * FROM booking WHERE patients_id = % s AND booking_id = %s', (patients_id, booking_id,))
#             Result = cur.fetchall()
#             return render_template('editB.html', Result=Result)
#         else:
#             msg = 'Incorrect patient id/ booking id'
#         cur.close()
#     return render_template('booking_details.html', msg=msg)


@app.route('/delete/<string:booking_id>', methods = ['GET'])
def delete(booking_id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM booking WHERE booking_id=%s", (booking_id,))
    mysql.connection.commit()
    return redirect(url_for('booking_details'))


@app.route('/editB/<string:booking_id>',methods=['POST','GET'])
def editB(booking_id):

    if request.method == 'POST':
        #booking_id = request.form['booking_id']
        patient_id = request.form['patient_id']
        slot = request.form['slot']
        date = request.form['date']
        disease = request.form['disease']
        dept_id = request.form['dept_id']

        cur = mysql.connection.cursor()
        cur.execute("""
                 UPDATE booking
                SET patient_id=%s, slot=%s, date=%s, disease=%s, dept_id=%s
                 WHERE booking_id=%s
                 """, (patient_id, slot, date, disease, dept_id, booking_id))
        mysql.connection.commit()
        cur.close()
        flash("Data Updated Successfully")
        return redirect(url_for('booking_details'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM booking WHERE booking_id = % s", (booking_id,))
    res = cur.fetchone()
    return render_template("editB.html", row=res)



if __name__ == '__main__':
    app.run(debug=True, port=8001)