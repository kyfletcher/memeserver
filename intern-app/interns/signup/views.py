from flask import Blueprint
from flask import render_template, make_response
from flask import request,redirect
from .. import database
import hashlib
import re
import uuid

signup = Blueprint('signup', __name__, template_folder="templates")

@signup.route('/signup', methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("signup/index.html")
    elif request.method == "POST":
        
        #check username
        username = (request.form['username'])
        if username.isalnum() == False:
            fail = True
            return render_template("signup/index.html", fail=fail)

        #check email
        email = (request.form['email'])
        emailcheck = re.split('[@|.]', email)
        for check in emailcheck:
            if check.isalnum() == False:
                fail = True
                return render_template("signup/index.html", fail=fail)
        
        
        
        #check password
        password = (request.form['password'])
        hashpw = hashlib.sha256(email+password)
        hexDig = hashpw.hexdigest()
        print hexDig

        #print(request.form)
        
        result = database.checkUserAndEmail(username, email)
        if result == True:
            database.createUser(username, hexDig, email)
            cookie = str(uuid.uuid4())
            database.setCookie(cookie, username)
            resp = make_response(redirect('/profile/'+username))
            resp.set_cookie('sessionID', cookie)
            return resp
        
        fail = True
        return render_template("signup/fail.html", fail=fail)
#      return redirect("http://localhost:8000/profile/kyle")

    
