from flask import Blueprint
from flask import render_template, make_response
from flask import request
from .. import database

allMemes = Blueprint('allMemes', __name__, url_prefix='/allMemes')

@allMemes.route('')
def url():

    allMemes = database.getAllMemes()
    cookie = request.cookies.get('sessionID')
    user = database.getCookieUser(cookie)
    role = database.checkRole(user)
    fail = request.args.get('fail')
    memeList = [dict(r) for r in allMemes]

    tagsDict = {}
    for memeInfo in memeList:
        memeName = memeInfo.get('meme_name')
        tags = ', '.join([str(r.tagName) for r in database.getTags(memeName)])
        tagsDict.update({memeName: tags})


    return render_template("allMemes/index.html", user=user,  memes = memeList, tags=tagsDict, role=role, fail=fail)