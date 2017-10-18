from flask import Blueprint
from flask import render_template, make_response
from flask import request,redirect
from .. import database
import hashlib
import re
import uuid

logout = Blueprint('logout', __name__, template_folder="templates")

@logout.route('/logout', methods=["GET"])
def main():
    if request.method == "GET":
        cookie = request.cookies.get('sessionID')
        cookieRE = re.split('[-]', cookie)
        cookieCheck = [x for x in cookieRE if x]
        for check in cookieCheck:
            if check.isalnum() == False:
                return redirect(url_for("login.main"))

        delCookie = database.deleteCookie(cookie)
        
        if delCookie == False:
            return redirect(url_for("login.main"))

        return render_template("logout/index.html")