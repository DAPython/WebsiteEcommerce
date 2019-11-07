from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)
app.secret_key = 'random string'

# Home page
@app.route("/")
def root():
    return render_template('index.html')

#Login check session
@app.route("/loginPage")
def loginPage():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

# login
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)


#Get Detail Login
def getLoginDetail():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            name = ''
        else:
            loggedIn = True
            cur.execute("SELECT user_id, name FROM user WHERE email = '" + session['email'] + "'")
            user_id, name = cur.fetchone()
    conn.close()
    return (loggedIn, name)

# is_valid
def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM user')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

#Register
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
    
    with sqlite3.connect('database.db') as con:
        try:
            cur = con.cursor()
            cur.execute('INSERT INTO user(password, email, name, address, phone) VALUES (?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, name, address, phone))
            
            con.commit()

            msg = "Registered Successfully"
        except:
            con.rollback()
            msg = "Error Occured"
    con.close()
    return render_template("login.html", error=msg)

@app.route("/registerPage")
def registerPage():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
