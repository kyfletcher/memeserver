from flask import Blueprint
from flask import render_template, make_response
from flask import request, flash
import re
from .. import database

addTags = Blueprint('addTags', __name__, url_prefix='/addTags')

@addTags.route('', methods=["GET", "POST"])
def url():
    cookie = request.cookies.get('sessionID')
    user = database.getCookieUser(cookie)
    if request.method == "GET":
        allTags = ([str(r.tagName) for r in database.getAllTags()])
        return render_template("addTags/index.html", user=user, tags=allTags)
    if request.method == "POST":
        tagName = request.form['tagName']
        

        #check user inputs
        tagspace = "".join(tagName.split())
        tagre = re.split('[!|?]', tagspace)
        tagcheck = [x for x in tagre if x]
        for check in tagcheck:
            if check.isalnum() == False:
                fail = True
                allTags = ([str(r.tagName) for r in database.getAllTags()])
                return render_template("addTags/index.html", user=user, tags=allTags, fail=fail)

        database.addTagName(tagName)
        allTags = ([str(r.tagName) for r in database.getAllTags()])
        return render_template("addTags/index.html", user=user, tags=allTags)