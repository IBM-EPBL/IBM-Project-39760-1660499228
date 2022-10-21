from email.mime import image
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re 
app = Flask(__name__)

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wml89493;PWD=FMiTW8w27vP4G70x;","","")

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        username = request.form['email']
        password = request.form['password']
        stmt = ibm_db.exec_immediate(conn,'SELECT * FROM SANGEETHA_DB WHERE email = % s AND password = % s', (email, password, ))
        account = ibm_db.fetch_both(stmt)
        if username==password:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'roll_no' in request.form :
        roll_no = request.form['roll_no']
        username = request.form['username']
        password = request.form['password']
        cpassword = request.form['cpassword']
        email = request.form['email']
        conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wml89493;PWD=FMiTW8w27vP4G70x;","","")
        stmt = ibm_db.exec_immediate(conn,'SELECT * FROM SANGEETHA_DB')
        if email==cpassword:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            sql=ibm_db.exec_immediate(conn,'INSERT INTO SANGEETHA_DB (roll_no, username, email, password, cpassword) VALUES (%s, % s, % s, % s)')
            msg = 'You have successfully registered !'
            print("you have successfully registered!")
            return redirect(url('/login'))
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)

if __name__=='__main__':
    app.run(debug=True)
