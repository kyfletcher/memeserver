from flask import Blueprint
from flask import render_template, make_response, Flask, request, redirect, url_for
from .. import database
import os
import re


upload = Blueprint('upload', __name__, url_prefix='/upload')


def allowed_file(filename):
	allowExts = set(['png', 'jpg', 'jpeg', 'gif'])
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowExts


@upload.route('', methods=['GET', 'POST'])
def upload_file():
	cookie = request.cookies.get('sessionID')
	user = database.getCookieUser(cookie)
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			fail = True
			return redirect(request.url, fail=fail)
		file = request.files['file']

		allTags = request.form.getlist('tags')
		print allTags
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			fail = True
			return render_template("upload/index.html", fail=fail)
		if file and allowed_file(file.filename):
			filename = file.filename
			filePath = './interns/static/memes/'
			memeName = (request.form['memeName'])
			memespace = "".join(memeName.split()) 
			memere = re.split('[!|?]', memespace)
			memecheck = [x for x in memere if x]
			for check in memecheck:
				if check.isalnum() == False:
					fail = True
					return render_template("upload/index.html", fail=fail)
			file.save(os.path.join(filePath, filename))
			
			database.insertMeme(user, memeName, filename)
			database.addTag(memeName, allTags)
			return redirect(url_for('profile.url', user=user))
		return
		
   

	allTags = ([str(r.tagName) for r in database.getAllTags()])
	return render_template("upload/index.html", tags=allTags)