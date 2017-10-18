from flask import Blueprint
from flask import render_template, make_response
from flask import request, flash
import re
from .. import database

search = Blueprint('search', __name__, url_prefix='/search')

@search.route('', methods=["POST"])
def url():
    cookie = request.cookies.get('sessionID')
    user = database.getCookieUser(cookie)
    
    searchTerm = request.form['searchTerm']
    allMemes = database.getAllMemes()
    memeList = [dict(r) for r in allMemes]
    tagsDict = {}
    allMemeInfo = []
    for memeInfo in memeList:
        
        memeName = memeInfo.get('meme_name')
        tags = ', '.join([str(r.tagName) for r in database.getTags(memeName)])

        if searchTerm.lower() in memeName.lower() or searchTerm.lower() in tags.lower():
            allMemeInfo.append(memeInfo)
            tagsDict.update({memeName: tags})
    return render_template("search/index.html", user=user,  memes = allMemeInfo, tags=tagsDict)