import logging

from pylons import request, response, session, tmpl_context as c, config
from pylons.controllers.util import abort

from fmod.lib.base import BaseController, render
from fmod import model

log = logging.getLogger(__name__)

import os

class ProfileController(BaseController):

	requires_auth=True

	def index(self):
		return render('profile.mako')

	def bookmarklet(self):
		# logged in...
		c.username = session['user']
		user= model.User.get_byName(c.username)
		if user:
			c.secret=user.secret
		else:
			c.secret = 'SECRET'
		c.url=os.path.join(config['base_uri'], 'p')
		c.nsid = user.nsid
		return render('bookmarklet.mako')
