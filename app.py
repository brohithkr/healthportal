from dbmanager import *
from flask import Flask, redirect, url_for, request, render_template, session
from flask_session import Session
 
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = sqlite3.connect("records.db",check_same_thread=False)
cur = conn.cursor()

# mconn = sqlite3.connect("medicalevents.db",check_same_thread=False)
# mcur = conn.cursor()

logged = []

@app.route("/")
def root():
    return render_template("welcome.html")

@app.route("/dlogin",methods = ['POST','GET'])
def dlogin():
    id = ''
    password = ''
    error = None
    if request.method=="POST":
        id=request.form['id']
        password=request.form['password']
    if id.isnumeric():
        if isdoc(cur, id):
            if cur.execute("select password from doctors where id=?",(id,)).fetchone()[0]==str(password):
                islogged = True
                name = cur.execute("select name from doctors where id=?",(id,)).fetchone()[0]
                session["id"]=id
                return redirect(url_for('dlogged'))
                 
                # return render_template("dashboard.html",name=name,idno=id)

            else:
                error="Invalid Password"
        else:
            error="Invalid ID"
    else:
        error="Invalid ID"
    if id=='':
        error=None

    return render_template("dlogin.html",error=error)

gpid = None
@app.route("/dlogged",methods=['POST','GET'])
def dlogged():
    id = session["id"]
    pid = None
    uname = cur.execute(f'select name from doctors where id={id}').fetchone()[0]
    if request.method=='POST':
        pid = request.form['pid']
        pid = int(pid)
        # gpid=pid
    
    name=''
    age=''
    bldgrp=''
    chronic=''
    allergies=''
    illdrugs=''
    history=None
    if pid:

        name = cur.execute('select name from patients where id=?',(pid,)).fetchone()[0]
        age = cur.execute('select age from patients where id=?',(pid,)).fetchone()[0]
        bldgrp = cur.execute('select bloogroup from patients where id=?',(pid,)).fetchone()[0]
        allergies = cur.execute('select allergies from patients where id=?',(pid,)).fetchone()[0]
        illdrugs = cur.execute('select illdrugs from patients where id=?',(pid,)).fetchone()[0]
        chronic = cur.execute('select chronic from patients where id=?',(pid,)).fetchone()[0]
        history = getMedicalHistory(pid)

    return render_template("dashboard.html",uname=uname,pid=pid,name=name,bldgrp=bldgrp,allergies=allergies,illdrugs=illdrugs,age=age,chronic=chronic,history=history)
    # return render_template("dashboard.html",uname=uname,idno=id)

@app.route("/logout")
def logout():
    session["id"]=None
    return redirect("/")

@app.route("/add<pid>",methods = ['POST','GET'])
def add(pid):
    if session["id"]:
        mconn=sqlite3.connect("medicalevents.db")
        mcur = mconn.cursor()
        doctor=cur.execute(f'SELECT name FROM doctors WHERE id={session["id"]}').fetchone()[0]
        symptoms=''
        disease=''
        diagnosis=''
        medication=''
        remarks=''
        if request.method=="POST":
            symptoms=request.form["symptoms"]
            disease=request.form["disease"]
            diagnosis=request.form["diagnosis"]
            medication=request.form["medication"]
            remarks=request.form["remarks"]
        if symptoms=='' and disease=='' and diagnosis=='' and medication=='' and remarks=='':
            # name=
            return render_template("add.html",pid=pid)
        else:
            addMedicalEvent(pid, doctor, symptoms, disease, diagnosis, medication, remarks)
            return redirect("/dlogged")

    else:
        return redirect("/dlogin")

@app.route('/plogin',methods=['POST','GET'])
def plogin():
    id = ''
    password = ''
    error = None
    if request.method=="POST":
        id=request.form['id']
        password=request.form['password']
    if id.isnumeric():
        if ispatient(cur, id):
            if cur.execute("select password from patients where id=?",(id,)).fetchone()[0]==str(password):
                islogged = True
                # name = cur.execute("select name from patient where id=?",(id,)).fetchone()[0]
                session["pid"]=id
                return redirect(url_for('plogged'))
                 
                # return render_template("dashboard.html",name=name,idno=id)

            else:
                error="Invalid Password"
        else:
            error="Invalid ID"
    else:
        error="Invalid ID"
    if id=='':
        error=None

    return render_template("plogin.html",error=error)

@app.route('/plogged')
def plogged():
    
    pid = session["pid"]
    # uname = cur.execute(f'select name from doctors where id={pid}').fetchone()[0]
    # if request.method=='POST':
    #     pid = request.form['pid']
    pid = int(pid)


    name=''
    age=''
    bldgrp=''
    chronic=''
    allergies=''
    illdrugs=''
    history=None
    

    name = cur.execute('select name from patients where id=?',(pid,)).fetchone()[0]
    age = cur.execute('select age from patients where id=?',(pid,)).fetchone()[0]
    bldgrp = cur.execute('select bloogroup from patients where id=?',(pid,)).fetchone()[0]
    allergies = cur.execute('select allergies from patients where id=?',(pid,)).fetchone()[0]
    illdrugs = cur.execute('select illdrugs from patients where id=?',(pid,)).fetchone()[0]
    chronic = cur.execute('select chronic from patients where id=?',(pid,)).fetchone()[0]
    history = getMedicalHistory(pid)

    return render_template("pdashboard.html",name=name,pid=pid,bldgrp=bldgrp,allergies=allergies,illdrugs=illdrugs,age=age,chronic=chronic,history=history)

@app.route("/plogout")
def plogout():
    session["pid"]=None
    return redirect("/")
  
if __name__=="__main__":
    app.run()
