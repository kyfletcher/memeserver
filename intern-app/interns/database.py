import time

from interns import db

def setup():
    db.create_all()

    
    #db.engine.execute("INSERT INTO user (username, email, password, role) VALUES ('asd', 'asd@asd.com', 'asd', 'admin')")
    db.engine.execute("INSERT INTO meme (meme_name, meme_path, uploaded_by, likes) VALUES ('Cookie Monster', 'cookiemonster.jpg', 1, 0)")
    db.engine.execute("INSERT INTO meme (meme_name, meme_path, uploaded_by, likes) VALUES ('Freezes', 'freezes.jpg', 1, 0)")
    db.engine.execute("INSERT INTO meme (meme_name, meme_path, uploaded_by, likes) VALUES ('Stealing Dataz', 'stealingdataz.jpeg', 1, 0)")
    db.engine.execute("INSERT INTO meme (meme_name, meme_path, uploaded_by, likes) VALUES ('You can do it!', 'youcandoit.jpg', 1, 0)")
    db.engine.execute("INSERT INTO meme (meme_name, meme_path, uploaded_by, likes) VALUES ('Not sure...', 'notsure.jpg', 2, 0)")
    db.engine.execute("INSERT INTO meme (meme_name, meme_path, uploaded_by, likes) VALUES ('Web Devs', 'webdevs.jpg', 2, 0)")
    
    db.engine.execute("INSERT INTO tags (tagName) VALUES ('Funny')")
    db.engine.execute("INSERT INTO tags (tagName) VALUES ('Cool')")
    db.engine.execute("INSERT INTO tags (tagName) VALUES ('Another')")
    
    db.engine.execute("INSERT INTO tag_join (tagID, mid) VALUES (1, 1)")
    db.engine.execute("INSERT INTO tag_join (tagID, mid) VALUES (2, 1)")

    db.engine.execute("INSERT INTO tag_join (tagID, mid) VALUES (1, 2)")

    try:
        db.session.commit()
        return
    except:
        db.session.rollback()


# CREATE TABLE tags (tagID INTEGER PRIMARY KEY AUTOINCREMENT, tagName TEXT)
# CREATE TABLE tag_join (tagID INTEGER, mid INTEGER)



def checkPw(email, password):
    db.create_all()
    userpw = db.engine.execute("SELECT password FROM user WHERE email = '"+email+"'").fetchone()
    username = db.engine.execute("SELECT username FROM user WHERE email = '"+email+"'").fetchone()
    if not userpw:
    	return False, None
    if password == userpw[0]:
    	return True, username
    return False, None


def checkUserAndEmail(username, email):
	db.create_all()
	userExist = db.engine.execute("SELECT * FROM user WHERE username = '"+username+"'").fetchone()
	emailExist = db.engine.execute("SELECT * FROM user WHERE email = '"+email+"'").fetchone()

	#check if they exist, if not then make them.
	if not userExist and not emailExist:
		return True
	else:
		return False

def createUser(username, password, email):
	db.create_all()
	db.engine.execute("INSERT INTO user (username, email, password, role) VALUES ('"+username+"', '"+email+"', '"+password+"', 'user')")
	
	try:
		db.session.commit()
	except:
		db.session.rollback()

def setCookie(cookie, userName):
	db.create_all()
	db.engine.execute("INSERT INTO cookies (cookieValue, cookieUser) VALUES ('"+cookie+"', '"+userName+"')")
	
	try:
		db.session.commit()
	except:
		db.session.rollback()

def checkCookieTimeout(cookie):
	db.create_all()
	lastAction = db.engine.execute("SELECT lastAction FROM cookies WHERE cookieValue = '"+cookie+"'").fetchone()
	currentTime = time.time()
	timeSinceLastAction = currentTime - int(lastAction[0])
	if timeSinceLastAction < 600:
		db.engine.execute("UPDATE cookies set lastAction = '"+str(int(currentTime))+"' WHERE cookieValue = '"+cookie+"'")
		try:
			db.session.commit()
		except:
			db.session.rollback()
		return True

	db.engine.execute("DELETE FROM cookies WHERE cookieValue = '"+cookie+"'")
	try:
		db.session.commit()
	except:
		db.session.rollback()
	return False

	
def checkCookie(cookie):
	db.create_all()
	cookieExists = db.engine.execute("SELECT * FROM cookies WHERE cookieValue = '"+cookie+"'").fetchone()
	if cookieExists:
		return True
	return False

def getUserMemes(username):
	db.create_all()
	uid = db.engine.execute("SELECT uid FROM user WHERE username = '"+username+"'").fetchone()
	if not uid:
		return False
	memeList = db.engine.execute("SELECT * FROM meme WHERE uploaded_by = '"+str(uid[0])+"'").fetchall()
	return memeList

def checkAuth(user, cookie):
	db.create_all()
	cookieUser = db.engine.execute("SELECT cookieUser FROM cookies WHERE cookieValue = '"+cookie+"'").fetchone()
	if user == cookieUser[0]:
		return
	return False

def getAllMemes():
	db.create_all()
	allList = db.engine.execute("SELECT * FROM meme").fetchall()
	return allList

def getCookieUser(cookie):
	db.create_all()
	cookieUser = db.engine.execute("SELECT cookieUser FROM cookies WHERE cookieValue = '"+cookie+"'").fetchone()
	if cookieUser[0]:
		return cookieUser[0]
	return False

def insertMeme(user, memeName, filename):
	db.create_all()
	userID = db.engine.execute("SELECT uid FROM user WHERE username = '"+user+"'").fetchone()
	db.engine.execute("INSERT INTO meme (meme_name, meme_path, uploaded_by, likes) VALUES ('"+memeName+"', '"+filename+"', "+str(userID[0])+", 0)")
	
	try:
		db.session.commit()
		return
	except:
		db.session.rollback()
		return

def deleteCookie(cookie):
	db.engine.execute("DELETE FROM cookies WHERE cookieValue = '"+cookie+"'")
	try:
		db.session.commit()
		return True
	except:
		db.session.rollback()
		return False
	return False

def getTags(memeName):
	memeID = db.engine.execute("SELECT mid FROM meme WHERE meme_name = '"+memeName+"'").fetchone()
	tags = db.engine.execute("SELECT tagName FROM tags INNER JOIN tag_join on tag_join.tagID = tags.tagID INNER JOIN meme on meme.mid = tag_join.mid where meme.mid = '"+str(memeID[0])+"'").fetchall()
	return tags

#get all tag names
def getAllTags():
	tags = db.engine.execute("SELECT tagName FROM tags").fetchall()
	return tags

#add tag to meme
def addTag(memeName, allTags):
	memeID = db.engine.execute("SELECT mid FROM meme WHERE meme_name = '"+memeName+"'").fetchone()
	for tag in  allTags:
		tagID = db.engine.execute("SELECT tagID FROM tags WHERE tagName = '"+tag+"'").fetchone()
		db.engine.execute("INSERT INTO tag_join (tagID, mid) VALUES ('"+str(tagID[0])+"', '"+str(memeID[0])+"')")
	
	try:
		db.session.commit()
		return
	except:
		db.session.rollback()
		return

#add tag name to database
def addTagName(tagName):
	db.engine.execute("INSERT INTO tags (tagName) VALUES ('"+tagName+"')")
	try:
		db.session.commit()
		return
	except:
		db.session.rollback()
		return


def getMemePath(memeName):
	path = db.engine.execute("SELECT meme_path FROM meme WHERE meme_name = '"+memeName+"'").fetchone()
	return path

def checkRole(username):
	role = db.engine.execute("SELECT role FROM user WHERE username = '"+username+"'").fetchone()
	return role[0]

#add tag name to database
def deleteMeme(memeName):
	db.engine.execute("DELETE FROM meme WHERE meme_name = ('"+memeName+"')")
	try:
		db.session.commit()
		return
	except:
		db.session.rollback()
		return


#user (uid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT, role TEXT, date_registered DATE DEFAULT(datetime('now','localtime')));
#meme (mid INTEGER PRIMARY KEY AUTOINCREMENT, meme_name TEXT, meme_path TEXT, uploaded_by INTEGER, likes INTEGER, upload_date DATE DEFAULT(date('now','localtime')));
#cookies (cid INTEGER PRIMARY KEY AUTOINCREMENT, cookieUser TEXT, cookieValue TEXT, creation_time DATE DEFAULT(strftime('%s','now')), lastAction DATE DEFAULT(strftime('%s','now')));

#tags (tagID INTEGER PRIMARY KEY AUTOINCREMENT, tagName TEXT)
#tag_join (tagID INTEGER, mid INTEGER)
