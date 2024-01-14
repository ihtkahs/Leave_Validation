from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "Mysql@123"  

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mysql@123'
app.config['MYSQL_DB'] = 'leaveletter'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = True

mysql = MySQL(app)
pth=os.path.join('static')


@app.route('/')
def index():
    return render_template('index.html',pth=pth)

@app.route('/counsellor')
def counsellor():
    return render_template('counsellor.html',pth=pth)

@app.route('/principal')
def principal():
    return render_template('principal.html',pth=pth)

@app.route('/HOD')
def HOD():
    return render_template('HOD.html',pth=pth)

@app.route('/student')
def Student():
    return render_template('Student.html',pth=pth)

@app.route('/yearincharge')
def yearincharge():
    return render_template('YearIncharge.html',pth=pth)

@app.route('/loginstudent', methods=['POST'])
def loginstudent():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['username'] = username
        return redirect(url_for('student_dashboard'))
    else:
        return 'Invalid username or password'

@app.route('/studentdb')
def student_dashboard():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE username = %s", (session['username'],))
        user = cur.fetchone()
        cur.close()

        if user:
            name = user[0]
            department = user[3]
            roll_no = user[4]
            reg_no = user[5]
            section = user[6]
            leaves_taken = user[7]

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM leave_application WHERE reg_no = %s", (reg_no,))
            leave_application = cur.fetchall()
            cur.close()

            return render_template('studentdashboard.html', pth=pth, name=name, department=department, roll_no=roll_no, reg_no=reg_no, section=section, leaves_taken=leaves_taken, leave_application=leave_application)
        else:
            return 'User details not found in the database.'
    else:
        return redirect(url_for('index'))
    
@app.route('/loginhod', methods=['POST'])
def loginHOD():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hod WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['username'] = username
        return redirect(url_for('HOD_dashboard'))
    else:
        return 'Invalid username or password'

@app.route('/HODdb')
def HOD_dashboard():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM leave_application WHERE counsellor_approve = 1 AND hod_approve = 0")
        leave_application = cur.fetchall()
        cur.close()

        return render_template('HODdb.html',pth=pth, leave_application=leave_application)
    else:
        return redirect(url_for('index'))

@app.route('/logincounsellor', methods=['POST'])
def logincounsellor():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM counsellor WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['username'] = username
        return redirect(url_for('counsellor_dashboard'))
    else:
        return 'Invalid username or password'

@app.route('/counsellordb')
def counsellor_dashboard():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM leave_application WHERE counsellor_approve = 0")
        leave_application = cur.fetchall()
        cur.close()

        return render_template('counsellordb.html', pth=pth, leave_application=leave_application)
    else:
        return redirect(url_for('index'))

@app.route('/loginprincipal', methods=['POST'])
def loginprincipal():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM principal WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['username'] = username
        return redirect(url_for('principal_dashboard'))
    else:
        return 'Invalid username or password'

@app.route('/principaldb')
def principal_dashboard():
    if 'username' in session:
        return render_template('principaldb.html',pth=pth)
    else:
        return redirect(url_for('index'))

@app.route('/loginyearincharge', methods=['POST'])
def loginyearincharge():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM yearincharge WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['username'] = username
        return redirect(url_for('yearincharge_dashboard'))
    else:
        return 'Invalid username or password'

@app.route('/yearinchargedb')
def yearincharge_dashboard():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM leave_application WHERE counsellor_approve = 1 AND hod_approve = 1 AND yearincharge_approve=0")
        leave_application = cur.fetchall()
        cur.close()

        return render_template('yearinchargedb.html',pth=pth, leave_application=leave_application)
    else:
        return redirect(url_for('index'))
    
from flask import request

def get_student_details(name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, registernumber, numberofleave FROM student WHERE username = %s", (name,))
    result = cur.fetchone()
    cur.close()

    if result:
        return result
    else:
        return None

@app.route('/apply_leave_multiple', methods=['POST'])
def apply_leave_multiple():
    reason = request.form['reasonMultiple']
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    noOfDays = request.form['noOfDays']
    name = session['username']
    student_details = get_student_details(name)
    if student_details:
        student_name, reg_no, leaves_taken = student_details    
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO leave_application (name, reg_no, start_date, end_date, reason, leaves_taken, noOfDays) VALUES (%s, %s, %s, %s, %s, %s, %s)", (student_name, reg_no, start_date, end_date, reason, str(leaves_taken), str(noOfDays)))
        mysql.connection.commit()
        cur.close()
        return 'Leave application submitted successfully.'
    else:
        return 'User details not found in the database.'

@app.route('/apply_leave_one', methods=['POST'])
def apply_leave_one():
    reason = request.form['reasonSingle']
    Date  = request.form['Date']
    name = session['username']
    student_details = get_student_details(name)
    if student_details:
        student_name, reg_no, leaves_taken = student_details    
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO leave_application (name, reg_no, date, reason, leaves_taken) VALUES (%s, %s, %s, %s, %s)", (student_name, reg_no, Date, reason, str(leaves_taken)))
        mysql.connection.commit()
        cur.close()
        return 'Leave application submitted successfully.'
    else:
        return 'User details not found in the database.'
    
@app.route('/apply_medical_leave', methods=['POST'])
def apply_medical_leave():
    reason = request.form['reasonMedical']
    start_date = request.form['medicalStartDate']
    end_date = request.form['medicalEndDate']
    medical_file = request.files['medicalDocuments']
    noOfDays = request.form['noOfDays']
    name = session['username']
    student_details = get_student_details(name)
    
    if medical_file:
        filename = secure_filename(medical_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        medical_file.save(file_path)

        if student_details:
            student_name, reg_no, leaves_taken = student_details    
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO leave_application (name, reg_no, start_date, end_date, reason, leaves_taken, noOfDays, medical) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (student_name, reg_no, start_date, end_date, reason, str(leaves_taken), noOfDays, file_path))
            mysql.connection.commit()
            cur.close()

            return 'Medical leave applied successfully.'
        else:
            return 'User details not found in the database.'
    else:
        return 'No file was uploaded.'
    
@app.route('/approve_leave_counsellor', methods=['POST'])
def approve_leave_counsellor():
    application_no = request.form['application_no']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE leave_application SET counsellor_approve = 1 WHERE application_no = %s", (application_no,))
    mysql.connection.commit()
    cur.close()

    return 'Leave request has been approved.'

@app.route('/approve_leave_hod', methods=['POST'])
def approve_leave_hod():
    application_no = request.form['application_no']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE leave_application SET hod_approve = 1 WHERE application_no = %s", (application_no,))
    mysql.connection.commit()
    cur.close()

    return 'Leave request has been approved.'

@app.route('/approve_leave_yearincharge', methods=['POST'])
def approve_leave_yearincharge():
    application_no = request.form['application_no']
    registration_no = request.form['registration_no']
    noOfDays = request.form['noOfDays']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE leave_application SET yearincharge_approve = 1 WHERE application_no = %s", (application_no,))
    mysql.connection.commit()
    cur.execute("UPDATE leave_application SET leaves_taken = leaves_taken + 1 WHERE application_no = %s", (application_no,))
    mysql.connection.commit()
    cur.execute("UPDATE student SET numberofleave = numberofleave + %s WHERE registernumber = %s", (noOfDays, registration_no,))
    mysql.connection.commit()
    cur.close()

    return 'Leave request has been approved.'

@app.route('/reject_leave_counsellor', methods=['POST'])
def reject_leave_counsellor():
    application_no = request.form['application_no']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE leave_application SET counsellor_approve = -1, hod_approve = -1, yearincharge_approve = -1 WHERE application_no = %s", (application_no,))
    mysql.connection.commit()
    cur.close()

    return 'Leave request has been rejected.'

@app.route('/reject_leave_hod', methods=['POST'])
def reject_leave_hod():
    application_no = request.form['application_no']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE leave_application SET hod_approve = -1, yearincharge_approve = -1 WHERE application_no = %s", (application_no,))
    mysql.connection.commit()
    cur.close()

    return 'Leave request has been rejected.'

@app.route('/reject_leave_yearincharge', methods=['POST'])
def reject_leave_yearincharge():
    application_no = request.form['application_no']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE leave_application SET yearincharge_approve = -1 WHERE application_no = %s", (application_no,))
    mysql.connection.commit()
    cur.close()

    return 'Leave request has been rejected.'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
