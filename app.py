from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from functools import wraps
from hashlib import sha256
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from sqlhelpers import *
from forms import *
import time

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2585'
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

mysql = MySQL(app)

def log_in_user(username):
    users = Table("users","name","email","username","password")
    user = users.getone("username",username)
    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorised Access, Not Logged in","danger")
            return redirect(url_for("login"))
    return wrap


@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users","name","email","username","password")

    if request.method == "POST" and form.validate():
        username = form.username.data
        email = form.email.data
        name = form.name.data

        if True:
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password)
            log_in_user(username)
            return redirect(url_for('dashboard'))
        else:
            flash("User Already Exists","danger")
            return redirect(url_for('register'))
    return render_template("register.html", form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = Table("users","name","email","username","password")
        data = users.getone("username",username)
        cpassword = data.get('password')

        if cpassword is None:
            flash("Username not found!","danger")
            return redirect(url_for('login'))
        else:
            if sha256_crypt.verify(password,cpassword):
                log_in_user(username)
                flash("Logged In!","success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid Password","danger")
                return redirect(url_for('login'))


    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged Out Succesfully!","success")
    return redirect(url_for('login'))



@app.route("/transaction", methods = ['GET', 'POST'])
@is_logged_in
def transaction():
    form = SendMoneyForm(request.form)
    balance = get_balance(session.get('username'))

    if request.method == 'POST':
        try:
            send_money(session.get('username'), form.username.data, form.amount.data)
            flash("Money Sent!", "success")
        except Exception as e:
            flash(str(e), 'danger')

        return redirect(url_for('transaction'))

    return render_template('transaction.html', balance=balance, form=form, page='transaction')


@app.route('/buy',methods = ['GET','POST'])
@is_logged_in
def buy():
    form = BuyMoneyForm(request.form)
    balance = get_balance(session.get('username'))


    if request.method == 'POST':
        try:
            send_money("Bank",session.get('username'),form.amount.data)
            flash("Money Bought!","success")
        except Exception as e:
            flash(str(e),'danger')
        return redirect(url_for('buy'))

    return render_template("buy.html",balance=balance,form=form,page='buy')


@app.route("/dashboard")
@is_logged_in
def dashboard():
    blockchain = get_blockchain().chain
    balance = get_balance(session.get('username'))
    currtime = time.strftime("%I:%M %p")
    return render_template('dashboard.html',session=session, balance = balance, currtime = currtime,blockchain=blockchain, page = 'dahsboard')
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
