import sqlite3

# def connectdb(dbname):
#     connection = sqlite3.connect(dbname,check_same_thread=False)
#     cur = connection.cursor()
#     return cur

def addDoctor(cur,conn,id,name,password):
    cur.execute("INSERT INTO doctors VALUES(?,?,?)",(id,name,password))
    conn.commit()

    

def addPatient(cur,conn,id,name,password,age,bloodgroup,chronic,allergies,illdrugs):
    # patient inserted in record
    cur.execute("INSERT INTO patients VALUES(?,?,?,?,?,?,?,?)",(id,name,password,age,bloodgroup,chronic,allergies,illdrugs))
    conn.commit()

    # patient medical event table being created
    mconn = sqlite3.connect("medicalevents.db",check_same_thread=False)
    mcur = mconn.cursor()
    mcur.execute(f'CREATE TABLE IF NOT EXISTS {"patient"+str(id)}(doctor VARCHAR(30), symptoms TEXT, disease TEXT, diagnosis TEXT, medication TEXT, remarks TEXT, time TEXT DEFAULT CURRENT_TIMESTAMP)',)
    mconn.commit()
    mconn.close()

patient = "patient"

def addMedicalEvent(id,doctor,symptoms,disease,diagnosis,medication,remarks):
    mconn = sqlite3.connect("medicalevents.db",check_same_thread=False)
    mcur = mconn.cursor()

    mcur.execute(f'INSERT INTO {patient+str(id)} VALUES(?,?,?,?,?,?,datetime("now","localtime"))',(doctor,symptoms,disease,diagnosis,medication,remarks))
    mconn.commit()
    mconn.close()

def getMedicalHistory(id):
    mconn = sqlite3.connect("medicalevents.db")
    mcur = mconn.cursor()
    data = mcur.execute(f"SELECT * FROM {'patient'+str(id)}").fetchall()
    mconn.close()
    return data



def isdoc(cur,id):

    isdoc = False
    for row in cur.execute("select * from doctors"):
        if(row[0]==int(id)):
            isdoc = True
            break
    return isdoc

def ispatient(cur,id):

    ispat = False
    for row in cur.execute("select * from patients"):
        if(row[0]==int(id)):
            ispat = True
            break
    return ispat

            

if __name__=="__main__":
    conn = sqlite3.connect("records.db")
    cur = conn.cursor()
    # hello='doctors'
    # print(cur.execute(f'SELECT * from {hello} where id==2244').fetchone()[2])

    # addPatient(cur, conn, "12345", "M. Subbaro", "hello", 67, "A+", "lung cancer", "dust", "perindopril")
    # addPatient(cur, conn, "23456", "Seeta", "hello", 52, "O+", "High B.P.", "peanuts", "amlodipine")
    # addDoctor(cur, conn, "54321", "Jane", "111")
    # addPatient(cur, conn, 1234, "durga", "hello", 18, "A+","heart problem","Dust allergy","citrizine")
    # addPatient(cur, conn, 2345, "sita", "ram", "25", "B+", "None", "None", "None")
    # addPatient(cur, conn, 3456, "john", "joker", "35", "O-", "Mental Illness", "Bats", "None")

    # print(cur.execute('INSERT INTO patients VALUES( 2345, "sita", "ram", "25", "B+", "None", "None", "None") WHERE NOT EXISTS(SELECT * FROM patients WHERE id=2345) '))

