from flask import Flask, render_template,request,session
from flask_session import Session

import sqlite3

from werkzeug.utils import redirect

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect("bookslibrary.db", check_same_thread=False)

listOfTables1 = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='BOOKS' ").fetchall()

if listOfTables1!=[]:
   print("Table 1 exits")
else:
    con.execute(''' CREATE TABLE BOOKS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    BOOKNAME TEXT,
    AUTHOR TEXT,
    CATEGORY TEXT,
    PRICE TEXT,
    PUBLISHER TEXT); ''')
    print("Table has created")

listOfTables2 = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='USERBOOKS' ").fetchall()

if listOfTables2!=[]:
   print("Table 2 exits")
else:
    con.execute(''' CREATE TABLE USERBOOKS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UNAME TEXT,
    UMOBNO TEXT,
    UEMAIL TEXT,
    UADDRESS TEXT,
    UPASSWORD TEXT); ''')
    print("Table has created")

cur2 = con.cursor()
cur2.execute("SELECT UEMAIL,UPASSWORD FROM USERBOOKS")
res2 = cur2.fetchall()
print(res2)


@app.route("/")
def myhome():
    return render_template("WebHome.html")


@app.route("/managerloginpanel", methods=["GET", "POST"])
def allogin():
    if request.method == "POST":
        getUname = request.form["username"]
        getppass = request.form["password"]

        if getUname == "Mr.Blacksmith":
            if getppass == "Piyush@123":
                return redirect("/librarybookentry")
    return render_template("UserProfileLogin.html")


@app.route("/librarybookentry", methods=["GET", "POST"])
def bookentry():
    if request.method == "POST":
        getBookName = request.form["name"]
        getAuthor = request.form["author"]
        getCategory = request.form["cat"]
        getPrice = request.form["price"]
        getPublisher = request.form["pub"]
        print(getBookName)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)
        try:
            con.execute("INSERT INTO BOOKS(BOOKNAME,AUTHOR,CATEGORY,PRICE,PUBLISHER) VALUES('"+getBookName+"','"+getAuthor+"','"+getCategory+"','" +getPrice+"','"+getPublisher+"')")
            print("successfully inserted !")
            con.commit()
            return redirect("/ViewAllBooks")
        except Exception as e:
            print(e)
    return render_template("LibraryBookEntry.html")


@app.route("/booksearch", methods=["GET", "POST"])
def booksearch():
    if request.method == "POST":
        getBOOKName = request.form["bname"]
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM BOOKS WHERE BOOKNAME = '"+getBOOKName+"' ")
        res2 = cur2.fetchall()
        return render_template("ViewAllBooks.html", bookss=res2)
    return render_template("BookSearch.html")


@app.route("/bookinfoedit", methods=["GET","POST"])
def bookinfoedit():
    if request.method == "POST":
        getNewname = request.form["newname"]
        getNewAuthor = request.form["newauthor"]
        getNewCategory = request.form["newcat"]
        getNewPrice = request.form["newprice"]
        getNewPublisher = request.form["newpub"]
        con.execute("UPDATE BOOKS SET BOOKNAME = '"+getNewname+"',AUTHOR = '"+getNewAuthor+"',CATEGORY ='"+getNewCategory+"',PRICE = '"+getNewPrice+"',PUBLISHER = '"+getNewPublisher+"'  ")
        print("successfully Updated !")
        con.commit()
        return redirect("/viewallbooks")
    return render_template("BookDetailsEdit.html")


@app.route("/bookinfodelete", methods=["GET", "POST"])
def bookinfodelete():
    if request.method == "POST":
        getNAMEDEL = request.form["namedel"]
        cur3 = con.cursor()
        cur3.execute("DELETE FROM BOOKS WHERE BOOKNAME = '"+getNAMEDEL+"' ")
    return render_template("BookDelete.html")


@app.route("/viewallbooks")
def viewallbooks():
    cur = con.cursor()
    cur.execute("SELECT * FROM BOOKS")
    res = cur.fetchall()
    return render_template("ViewAllBooks.html", bookss=res)


@app.route("/usercardview")
def usercardview():
    cur3 = con.cursor()
    cur3.execute("SELECT * FROM BOOKS")
    res6 = cur3.fetchall()
    return render_template("UserCardView.html", books3=res6)


@app.route("/userregistration", methods=["GET", "POST"])
def userregistration():
    if request.method == "POST":
        getUName = request.form["usname"]
        getUmobno = request.form["mobileno"]
        getEmail = request.form["email"]
        getAdd = request.form["address"]
        getPass = request.form["pass"]
        con.execute("INSERT INTO USERBOOKS(UNAME,UMOBNO,UEMAIL,UADDRESS,UPASSWORD) VALUES('" + getUName + "','" + getUmobno + "','" + getEmail + "','" + getAdd + "','" + getPass + "')")
        print("successfully inserted !")
        con.commit()
        return redirect("/userprofilelogin")
    return render_template("UserRegistrationForm.html")


@app.route("/userprofileview")
def userprofileview():
    if not session.get("name"):
        return redirect("/userprofilelogin")
    else:
        cur = con.cursor()
        cur.execute("SELECT * FROM BOOKS")
        res = cur.fetchall()
        return render_template("UserProfileView.html", bookss=res)


@app.route("/userprofilelogin", methods=["GET", "POST"])
def uprofilelogin():
    if request.method == "POST":
        getuseremail = request.form["Uname"]
        getuserpass = request.form["Upass"]
        print(getuseremail)
        print(getuserpass)
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM USERBOOKS WHERE UEMAIL = '"+getuseremail+"' AND UPASSWORD = '"+getuserpass+"'")
        res2 = cur2.fetchall()
        if len(res2) > 0:
            for i in res2:
                getName = i[1]
                getid = i[0]

            session["name"] = getName
            session["id"] = getid

            return redirect("/userprofileview")
    return render_template("UserProfileLogin.html")


@app.route("/userprofilesearch", methods=["GET", "POST"])
def userprofilesearch():
    if not session.get("name"):
        return redirect("/userprofilelogin")
    else:
        if request.method == "POST":
            getBOOKName = request.form["ubname"]
            cur2 = con.cursor()
            cur2.execute("SELECT * FROM BOOKS WHERE BOOKNAME = '" + getBOOKName + "' ")
            res2 = cur2.fetchall()
            return render_template("UserProfileView.html", bookss=res2)
        return render_template("UserProfileSearch.html")


@app.route("/userlogoutform", methods=["GET", "POST"])
def userlogoutform():

    if not session.get("name"):
        return redirect("/userprofilelogin")
    else:
        session["name"] = None
        return redirect("/")


if __name__ == "__main__":
    app.run()