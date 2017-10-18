from flask import Blueprint
from flask import render_template, make_response, Flask, request, redirect, url_for
from .. import database
import os
import re


tags = Blueprint('tags', __name__, url_prefix='/tags')


@tags.route('/<user>', methods=['GET' ]) #, 'POST'])
def tags_file(user):
	if request.method == "GET":
		userMemes = database.getUserMemes(user)
		print userMemes
		if userMemes == False:
			fail = True
			return render_template("tags/index.html", user=user, fail=fail)
		
		memeList = [dict(r) for r in userMemes] #list comprehension
		tagsDict = {} 
		print len(memeList)
		for memeInfo in memeList:
			memeName = memeInfo.get('meme_name')
			tags = ', '.join([str(r.tagName) for r in database.getTags(memeName)])
			tagsDict.update({memeName: tags})
		return render_template("tags/index.html", user=user, memes = memeList, tags=tagsDict, get=True) 

	# if request.method == "POST":
	# 	allTags = ([str(r.tagName) for r in database.getAllTags()])
	# 	memeName = request.form['submit']
	# 	formTags = request.form.getlist('tags')

	# 	for aTag in allTags:
	# 		for tag in formTags:
	# 			if tag == aTag:
	# 				return

	# 		tags = request.form[aTag]
	# 		if not tag:
	# 			print aTag
				
			#print tag
			#if they are equal, 
				#check to see if they are in tag_join. 
					#If they are, Don't do anything. 
					#else add them
			#if they are not equal
				#check if they are in tag_join
					#if they are, delete them
					#else, return
		# return render_template("tags/index.html", user=user, memes = memeList, tags=tagsDict, get=True) 

@tags.route('/<user>/<meme>', methods=['POST'])
def updateMemeName(user, meme):
	tags = ','.join([str(r.tagName) for r in database.getTags(meme)])
	tags = tags.split(',')
	tagsDict = {}
	tagsDict.update({meme: tags})
	path = database.getMemePath(meme)[0]
	allTags = ([str(r.tagName) for r in database.getAllTags()])
	return render_template("tags/index.html", user=user, memes=meme, tags=tagsDict, path=path, allTags=allTags, post=True)


@tags.route('')
def query_string():
    user = request.args.get('user', None)
    if not user:
        abort(404)

    return render_template("tags/index.html", user=user)
