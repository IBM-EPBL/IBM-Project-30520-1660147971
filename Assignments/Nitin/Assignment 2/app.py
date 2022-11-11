from flask import Flask
from flask import request, redirect, url_for, render_template
import ibm_db

app = Flask(__name__)
db_connection = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=byk67006;PWD=tHJ5cnoszK6nGIU3",'','')
#print("success: ", db_connection)

@app.route('/')
def index():
    return render_template('Homepage.html')

@app.route("/About")
def about():
    return render_template('About.html')

@app.route("/sign-in", methods=["GET","POST"])
def signIn():
    if request.method == "POST":
        data = request.form.to_dict()
        sql_query = "SELECT userPassword FROM USERS WHERE email = '{}'".format(data["email"])
        result = ibm_db.exec_immediate(db_connection,sql_query)
        value = ibm_db.fetch_tuple(result)[0].replace(" ","")

        if value == data["password"]:
            return redirect(url_for("index", msg="Logged in"))
        else:
            return render_template('Sign-in.html', msg="Invalid credentials")

    if request.method == "GET":
        return render_template('Sign-in.html')

@app.route("/sign-up", methods=["GET","POST"])
def signUp():
    if request.method == "GET":
        return render_template('Sign-up.html')
    if request.method == "POST":
        data = request.form.to_dict()
        sql_query = "INSERT INTO USERS (email, username, userPassword) VALUES('{}','{}','{}')".format(data["email"], data["username"], data["password"])
        ibm_db.exec_immediate(db_connection, sql_query)
        return redirect(url_for("signIn"))

if __name__ == "__main__":
    app.run(debug=True)