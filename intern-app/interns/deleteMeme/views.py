from flask import Blueprint
from flask import render_template, make_response
from flask import request, flash, redirect, url_for
import re
from .. import database

deleteMeme = Blueprint('deleteMeme', __name__, url_prefix='/deleteMeme')

@deleteMeme.route('', methods=["POST"])
def url():
    allMemes = database.getAllMemes()
    cookie = request.cookies.get('sessionID')
    user = database.getCookieUser(cookie)
    role = database.checkRole(user)
    if role == 'admin':
        memeData = request.form[('memeData')]
        memespace = "".join(memeData.split()) 
        memere = re.split('[!|?]', memespace)
        memecheck = [x for x in memere if x]
        for check in memecheck:
            if check.isalnum() == False:
                fail = True
                return redirect(url_for('allMemes.url', fail=fail))
        database.deleteMeme(memeData)

    return redirect(url_for("allMemes.url"))