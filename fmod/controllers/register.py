import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from fmod.lib.base import BaseController, render
from fmod import model

log = logging.getLogger(__name__)

import md5

class RegisterController(BaseController):

	def index(self):
		return render('register.mako')

	def submit(self):
		# Both fields filled?
		form_username = str(request.params.get('username'))
		form_password = str(request.params.get('password'))
		form_password_2 = str(request.params.get('password_2'))
		
		
		# Get user data from database
		db_user = model.User().get_byName(form_username)
		log.debug("%s,%s"%(db_user, form_username))
		if db_user is None: # User does not exist
			# great.
			u = model.User()
			if form_password != form_password_2:
				c.msg = "Sorry, those passwords didn't match." 
				return render('register.mako')
			u.username = form_username
			u.set_password(form_password)
			u.make_secret()
			u.save()
			u.commit()
		else:
			c.msg = "Sorry, that user is already registered." 
			return render('register.mako')
		
		# Mark user as logged in
		session['user'] = form_username
		session.save()
		
		redirect_to('/profile/index')

