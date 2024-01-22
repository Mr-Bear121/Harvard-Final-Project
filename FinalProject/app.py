import os

from cs50 import SQL

from flask import Flask, render_template,request, redirect, session
from flask_session import Session
import time,datetime

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///data/Chrono.db")


@app.route("/", methods=["GET","POST"])
def index():
    query = f""
    cDay = datetime.datetime.today()
    myTime = cDay.strftime('%H:%M')
    date = cDay.strftime('%Y-%m-%d')
    btnText = "Submit Time"

    if request.method=="POST":
        fTime = request.form.get("todayTime")
        fDate = request.form.get("todayDate")

        query = f"select * from timeSheet where signout = \"00:00\" and smonth = \"{fDate}\" "

        if not db.execute(query):
            query = f"INSERT INTO timeSheet (user,signin,smonth) VALUES (\"{session["username"]}\",\"{fTime}\",\"{fDate}\")"
            db.execute(query)
        else:
            query = f"UPDATE timeSheet SET signout = \"{fTime}\" where smonth = \"{date}\" and signout = \"00:00\""
            db.execute(query)

    btnText = timeInTimeOut()

    return render_template("index.html",time=myTime,date=date, btnText=btnText)

@app.route("/login", methods=["GET","POST"])
def login():
    query = None
    userName = None
    passWord = None

    if request.method == "POST":
        session.clear()
        userName = request.form.get("userName")
        passWord = request.form.get("passWord")

        if not userName:
            return render_template("unAvailable.html")
        elif not passWord:
            return render_template("unAvailable.html")

        query = f"SELECT * FROM usrAccounts WHERE username = \"{userName}\""
        rows = db.execute(query)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not (rows[0]["userpassword"]):
            return render_template("unAvailable.html")

        if usrExists(userName):
            session["user_id"] = rows[0]["id"]
            session["username"] = rows[0]["username"]
            return redirect("/")
        else:
            return redirect("/")

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    query = None
    userName = None
    passWord = None

    if request.method == "POST":
        session.clear()
        userName = request.form.get("userName")
        passWord = request.form.get("passWord")

        if not userName:
            return render_template("unAvailable.html")
        elif not passWord:
            return render_template("unAvailable.html")

        if not usrExists(userName):
            query = f'INSERT INTO usrAccounts (username,userpassword) VALUES ("{userName}","{passWord}")'
            db.execute(query)

            query = f'select id from usrAccounts where username=\"{userName}\"'
            data = db.execute(query)

            session["user_id"] = data[0]["id"]
            session["username"] = data[0]["username"]
            return redirect("/")

    return render_template("register.html")

@app.route("/timesheet", methods=["GET","POST"])
def timesheet():
    userName=session["username"]
    query = f'select signin as Timein,signout as Timeout, smonth as Date from timeSheet where user=\"{userName}\"'
    data = db.execute(query)
    tableHead = None
    try:
        tableHead = data[0].keys()
    except:
        return render_template("timeSheet.html", tableHead=tableHead)

    if request.method == "POST":
        pass

    return render_template("timeSheet.html",data=data,tableHead=tableHead)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/unAvailable")
def unAvailable():
    return render_template("unAvailable.html")


def timeInTimeOut():

    query = f"select * from timeSheet where signout = \"00:00\" "

    if not db.execute(query):
        return "Sign in"
    else:
        return "Sign Out"


def usrExists(userName):
    query = f'select username from usrAccounts where username=\"{userName}\"'
    data = db.execute(query)

    if not data:
        return False
    else:
        return True

