from flask import Blueprint
from flask import abort
from flask import render_template, make_response
from flask import request
from flask import session
from .. import database

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/<user>')
def url(user):
    cookie = request.cookies.get('sessionID')
    if database.checkAuth(user, cookie) == False:
        fail = True
        return render_template("profile/index.html", fail=fail)
	
    userMemes = database.getUserMemes(user)
    if userMemes == False:
        fail = True
        return render_template("profile/index.html", fail=fail)
    
    
    memeList = [dict(r) for r in userMemes] #list comprehension

    tagsDict = {}
    for memeInfo in memeList:
        memeName = memeInfo.get('meme_name')
        tags = ', '.join([str(r.tagName) for r in database.getTags(memeName)])
        tagsDict.update({memeName: tags})
    return render_template("profile/index.html", user=user, memes = memeList, tags=tagsDict)

@profile.route('')
def query_string():
    user = request.args.get('user', None)
    if not user:
        abort(404)

    return render_template("profile/index.html", user=user)
