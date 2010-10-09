import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from fmod.lib.base import BaseController, render
from fmod import model

log = logging.getLogger(__name__)
import md5

class LoginController(BaseController):
	# entirely from http://wiki.pylonshq.com/display/pylonscookbook/Simple+Homegrown+Authentication
	def index(self):
		"""
		Show login form. Submits to /login/submit
		"""
		c.msg = ''
		return render('login.mako')
    
	def submit(self):
		"""
		Verify username and password
		"""
		# Both fields filled?
		form_username = str(request.params.get('username'))
		form_password = str(request.params.get('password'))
       
		# Get user data from database
		db_user = model.User().get_byName(form_username)
		if db_user is None: # User does not exist
			c.msg = "Sorry, that user is not known"
			return render('login.mako')

		# Wrong password? (MD5 hashes used here)
		if not db_user.check_password(form_password):
			c.msg = "Sorry, that password is incorrect"
			return render('login.mako')

		# Mark user as logged in
		session['user'] = form_username
		session.save()

		# Send user back to the page he originally wanted to get to
		if session.get('path_before_login'):
			path = session['path_before_login']
			del(session['path_before_login'])
			redirect_to(path)
		else: # if previous target is unknown just send the user to a welcome page
			redirect_to(controller='profile', action='index')
			

	def logout(self):
		"""
		Logout the user and display a confirmation message
		"""
		if 'user' in session:
			del(session['user'])
		if 'token' in session:
			del(session['token'])
		session.save()
				
		return render('logout.mako')


 
