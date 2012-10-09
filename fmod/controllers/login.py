import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort

from fmod.lib.base import BaseController, render
from fmod import model

log = logging.getLogger(__name__)

class LoginController(BaseController):

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


 
