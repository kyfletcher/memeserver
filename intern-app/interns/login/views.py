from flask import Blueprint
from flask import render_template, make_response
from flask import request,redirect
from .. import database
import hashlib
import re
import uuid

login = Blueprint('login', __name__, template_folder="templates")

@login.route('/', methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("login/index.html")
    elif request.method == "POST":

        email = (request.form['email'])
        emailcheck = re.split('[@|.]', email)
        for check in emailcheck:
            if check.isalnum() == False:
                fail = True
                return render_template("login/index.html", fail=fail)
        
        password = (request.form['password'])
        hashpw = hashlib.sha256(email+password)
        hexDig = hashpw.hexdigest()
        result, uname = database.checkPw(email, hexDig)
        if result == True:
        	cookie = str(uuid.uuid4())
        	database.setCookie(cookie, uname[0])
        	resp = make_response(redirect('/profile/'+uname[0]))
        	resp.set_cookie('sessionID', cookie)
        	return resp
        
        fail = True
        return render_template("login/index.html", fail=fail)
    
