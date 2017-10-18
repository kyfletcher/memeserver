import datetime

from flask import Flask
from flask import abort
from flask import render_template, make_response
from flask import request, redirect, url_for
import os, re

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')



# Wrap the app
db = SQLAlchemy(app)
db.autoflush = True;
db.autocommit = True;

# Import app modules that may require DB
from interns import database

from interns.login.views import login
from interns.profile.views import profile
from interns.signup.views import signup
from interns.allMemes.views import allMemes
from interns.upload.views import upload
from interns.logout.views import logout
from interns.tags.views import tags
from interns.addTags.views import addTags
from interns.search.views import search
from interns.deleteMeme.views import deleteMeme


# Register blueprints
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(profile)
app.register_blueprint(signup)
app.register_blueprint(allMemes)
app.register_blueprint(upload)
app.register_blueprint(tags)
app.register_blueprint(addTags)
app.register_blueprint(search)
app.register_blueprint(deleteMeme)

@app.before_request
def validate_request():
	if request.path == url_for("login.main") or request.path == url_for("signup.main"):
		return

	if request.path == "/static/css/bootstrap.css":
		return
	if request.path == "/static/js/socket.io.min.js":
		return
	if request.path == "/static/js/javascript.js":
		return


	cookie = request.cookies.get('sessionID')

	if cookie == None: 
		return redirect(url_for("login.main"))

	cookieRE = re.split('[-]', cookie)
	cookieCheck = [x for x in cookieRE if x]
	for check in cookieCheck:
		if check.isalnum() == False:
			return redirect(url_for("login.main"))

	result = database.checkCookie(cookie)
	if result == False:
		resp = make_response(redirect('/'))
		resp.set_cookie('sessionID', '', expires=0)
		return resp
	timestampValue = database.checkCookieTimeout(cookie)
	if timestampValue == False:
		resp = make_response(redirect('/'))
		resp.set_cookie('sessionID', '', expires=0)
		return resp
	return

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(error):
  return render_template('404.html'), 403


# @app.after_request

# @app.before_first_request
# def on_start():
# 	database.setup()
	#database.getTags('Cookie Monster')
	

from flask_socketio import emit
from flask_socketio import rooms
from flask_socketio import send
from flask_socketio import SocketIO

socketio = SocketIO()
socketio.init_app(app, async_mode="eventlet", allow_upgrades=True, cors_allowed_origins=["127.0.0.1"])

@socketio.on('connect')
def connect():
        emit('connect', 'Hello ' + request.cookies.get('user', 'Stranger'))
