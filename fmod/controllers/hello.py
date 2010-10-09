import logging

from pylons import request, response, session, tmpl_context as c, config
from pylons.controllers.util import abort, redirect_to

from fmod.lib.base import BaseController, render
from fmod import model

import os

log = logging.getLogger(__name__)

import md5

class HelloController(BaseController):

	def index(self):
		# Return a rendered template
		#	return render('/template.mako')
		# or, Return a response
		return render('hello.mako')
		
	def serverinfo(self):
		return render('/serverinfo.mako') 

		
	def home(self):
		return render('home.mako')
