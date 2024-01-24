# from googletrans import Translator
import requests
from cs50 import SQL
from flask import request, Flask, redirect, render_template, session, url_for, send_from_directory
from flask_session import Session
# from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
# import sys

from helpers import login_required

#debug2
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///technoverse.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")

# REGISTER CLIENT 
@app.route("/registerclient", methods=["GET", "POST"])
def registerclient():
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # get data through post
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)
        acc_type="client"
        # empty email, password,confirmation
        if not request.form.get("email"):
            return redirect('/registerclient')
        elif not request.form.get("password"):
            return redirect('/registerclient')
        elif not request.form.get("confirmation"):
            return redirect('/registerclient')
        if password != confirmation:
            return redirect('/registerclient')
        try:
            db.execute("INSERT INTO users (email,hash, acc_type) VALUES (? ,? ,?)",
                       email, hash, acc_type)
            rows = db.execute("SELECT * FROM users WHERE email=?", email)
            session["user_id"] = rows[0]["id"]
            return redirect("/clientform")
        except:
            return redirect('/registerclient')
    else:
        # User reached route via POST (as by submitting a form via GET)
        return render_template("registerclient.html")

# REGISTER PROFESSIONAL 
@app.route("/registerprof", methods=["GET", "POST"])
def registerprof():
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # get data through post
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)
        acc_type="prof"
        # empty email, password,confirmation
        if not request.form.get("email"):
            return redirect('/registerprof')
        elif not request.form.get("password"):
            return redirect('/registerprof')
        elif not request.form.get("confirmation"):
            return redirect('/registerprof')
        if password != confirmation:
            return redirect('/registerprof')
        try:
            db.execute("INSERT INTO users (email,hash, acc_type) VALUES (? ,? ,?)",
                       email, hash, acc_type)
            rows = db.execute("SELECT * FROM users WHERE email=?", email)
            session["user_id"] = rows[0]["id"]
            return redirect("/profform")
        except:
            return redirect('/registerprof')
    else:
        # User reached route via POST (as by submitting a form via GET)
        return render_template("registerprof.html")

# LOGIN CLIENT 
@app.route("/loginclient", methods=["GET", "POST"])
def loginclient():
   # Forget any user_id
    session.clear()
    acc_type = "client"
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        # Ensure email was submitted
        if not request.form.get("email"):
            return redirect('/loginclient')
        # Ensure password was submitted
        elif not request.form.get("password"):
            return redirect('/loginclient')
        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = ?",
                          request.form.get("email"))
         # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect('/loginclient')
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/clientdashboard")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("loginclient.html")
    

# LOGIN Professional 
@app.route("/loginprof", methods=["GET", "POST"])
def loginprof():
    # Forget any user_id
    session.clear()
    acc_type = "prof"
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        # Ensure email was submitted
        if not request.form.get("email"):
            return redirect('/loginprof')
        # Ensure password was submitted
        elif not request.form.get("password"):
            return redirect('/loginprof')
        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = ?",
                          request.form.get("email"))
        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect('/loginprof')
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/profdashboard")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("loginprof.html")

# LOGIN ADMIN
@app.route("/loginadmin", methods=["GET", "POST"])
def loginadmin():
    # Forget any user_id
    session.clear()
    acc_type = "admin"
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        # Ensure email was submitted
        if not request.form.get("email"):
            return redirect('/loginadmin')
        # Ensure password was submitted
        elif not request.form.get("password"):
            return redirect('/loginadmin')
        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = ?",
                          request.form.get("email"))
        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect('/loginadmin')
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/admindashboard")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("loginadmin.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/clientform" , methods=["GET", "POST"])
@login_required
def clientform():
    if request.method == "POST":
        id = session["user_id"]
        username = request.form.get("username")
        name = request.form.get("Name")
        contact = request.form.get("contact")
        address = request.form.get("address")
        # print(services)
        db.execute("INSERT INTO client (client_id, username, name, contact, address) VALUES (?,?,?,?,?)",
                   id, username, name, contact, address)
        return redirect("/clientdashboard")
    else:
        return render_template("clientform.html")  

@app.route("/profform", methods=["GET", "POST"])
@login_required
def profform():
    if request.method == "POST":
        id = session["user_id"]
        username = request.form.get("username")
        name = request.form.get("Name")
        contact = request.form.get("contact")
        address = request.form.get("address")
        specialization = request.form.get("specialization")
        prof_type = request.form.get("prof_type")
        idlink  = request.form.get("idlink")
        experience  = request.form.get("experience")
        # print(services)
        db.execute("INSERT INTO prof (prof_id, username, name, contact, address, specialization,prof_type,idlink,workexp) VALUES (?,?,?,?,?,?,?,?,?)",
                   id, username, name, contact, address, specialization,prof_type,idlink,experience)
        return redirect("/profdashboard")
    else:
        return render_template("profform.html")
   
@app.route("/profdashboard")
@login_required
def profdashboard():
    id = session["user_id"]
    return render_template("profdashboard.html", prof_id=id)

@app.route("/clientdashboard")
@login_required
def clientdashboard():
    # id = session["user_id"]
    return render_template("clientdashboard.html")

@app.route("/admindashboard")
@login_required
def admindashboard():
    # id = session["user_id"]
    return render_template("admindashboard.html")



@app.route("/viewprofilep")
@login_required
def viewprofilep():
    id = session["user_id"]
    query = db.execute("SELECT * FROM prof where prof_id = ?", id)
    return render_template("viewprofilep.html", list=query)


@app.route("/viewprofilec")
@login_required
def viewprofilec():
    id = session["user_id"]
    query = db.execute("SELECT * FROM client where client_id = ?", id)
    return render_template("viewprofilec.html", list=query)

@app.route("/viewservices")
@login_required
def viewservices():
    return render_template("viewservices.html")

@app.route("/Lawyer")
@login_required
def Lawyer():
    return render_template("Lawyer.html")

@app.route("/IT")
@login_required
def IT():
    return render_template("IT.html")

@app.route("/FamilyLaw")
@login_required
def FamilyLaw():
    specialization="Family Law"
    query = db.execute("SELECT * FROM prof where specialization = ?", specialization)
    # print(query)
    return render_template("FamilyLaw.html", list=query)

@app.route("/CorporateLaw")
@login_required
def CorporateLaw():
    specialization="Corporate Law"
    query = db.execute("SELECT * FROM prof where specialization = ?", specialization)
    # print(query)
    return render_template("CorporateLaw.html", list=query)

@app.route("/AppDeveloper")
@login_required
def AppDeveloper():
    specialization="App Developer"
    query = db.execute("SELECT * FROM prof where specialization = ?", specialization)
    # print(query)
    return render_template("AppDeveloper.html", list=query)

# MAKE Request
@app.route("/sendreq", methods=["POST"])
@login_required
def sendreq():
    id = session["user_id"]
    prof_id = request.form.get("prof_id")
    # quot = request.form.get("quot")
    a=int(prof_id)
    prof_name = db.execute("SELECT name FROM prof WHERE prof_id = ?",
                            prof_id)[0]["name"]
    client_name = db.execute("SELECT name FROM client WHERE client_id = ?",
                            id)[0]["name"]    
    contact_c =db.execute("SELECT contact FROM client WHERE client_id = ?",
                            id)[0]["contact"]
    contact_p =db.execute("SELECT contact FROM prof WHERE prof_id = ?",
                            prof_id)[0]["contact"]
    print(prof_name)
    print(client_name)
    print(id)
    print(prof_id)            
    db.execute("INSERT INTO req (prof_id, client_id, name_c, name_p, contact_c, contact_p) VALUES (?,?,?,?, ?, ?)", prof_id, id, client_name, prof_name, contact_c, contact_p)
    return redirect("/clientdashboard")


# CHECK RECIEVED BIDS OR QUOTATIONS AS A CLIENT
@app.route("/viewreq")
@login_required
def viewreq():
    id = session["user_id"] 
    prof_name = db.execute("SELECT name FROM prof WHERE prof_id = ?",
                            id)[0]["name"]
    query = db.execute("SELECT * FROM req where name_p = ?", prof_name)
    return render_template("viewreq.html",list=query)

# CHOOSE CLIENT
@app.route("/updatestatus", methods=["POST"])
@login_required
def updatestatus():
    # prof id
    id = session["user_id"]
    req_id = request.form.get("req_id")
    # client_id = request.form.get("client_id")
    # client_name=request.form.get(client_name)
    db.execute("UPDATE req SET status = 1 WHERE req_id = ? ",  req_id)   
    return redirect("/profdashboard")
   
# ONGOING PROJECTS CLIENT
@app.route("/myworkc")
@login_required
def myworkc():
    id = session["user_id"]
    query = db.execute("SELECT * FROM req WHERE client_id = ? AND status=1", id)
    return render_template("myworkc.html", list=query)

# ONGOING PROJECTS WORKER
@app.route("/myworkp")
@login_required
def myworkp():
    id = session["user_id"]
    prof_name = db.execute("SELECT name FROM prof WHERE prof_id = ?",
                            id)[0]["name"]
    query = db.execute("SELECT * FROM req where name_p = ? AND status=1", prof_name)
    return render_template("myworkp.html", list=query)


@app.route("/changecompletionc", methods=["POST"])
@login_required
def changecompletionc():
    id = session["user_id"]
    req_id = request.form.get("req_id")
    rateworker = request.form.get("rateworker")
    print(rateworker)
     
    db.execute("UPDATE req SET complete = 1 WHERE req_id = ? ",  req_id)
    db.execute("UPDATE req SET rating=? WHERE req_id = ? ", rateworker, req_id)
    
    return redirect("/myworkc")

@app.route("/rating/<id>")
def rating(id):
    # id = session["user_id"] 
    id=int(id)
    print(id)
    prof_name = db.execute("SELECT name FROM prof WHERE prof_id = ?",
                            id)[0]["name"]
    query = db.execute("SELECT * FROM req where complete = 1 AND name_p = ?", prof_name)
    print(query)
    return render_template("rating.html",list=query)

@app.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html")

if __name__ == '__main__':
    app.run(debug=True)
