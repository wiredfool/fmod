import logging

from pylons import request, response, session, tmpl_context as c, config
from pylons.controllers.util import abort, redirect_to

from fmod.lib.base import BaseController, render
from fmod import model

log = logging.getLogger(__name__)

from flickrapi import FlickrAPI

try:
    from elementtree import ElementTree as et
except:
    import xml.etree.ElementTree as et


class FlickrController(BaseController):
	def login_user(self):
		# so that we have a 1:1 correspondence between the flickr usernames
		# and our application usernames. 
		fapi = FlickrAPI(config['api_key'], config['api_secret'])
		redirect_to(fapi.web_login_url('read'))
		
	def login(self):
		fapi = FlickrAPI(config['api_key'], config['api_secret'])
		redirect_to(fapi.web_login_url('write'))

	def members(self):
		return render('member.mako')
	def moderators(self):
		return render('moderators.mako')

	def cb(self):
		# this is the callback point for the flickr auth.
		# we'll get a parameter of ?frob=123412341234
		# we call flickr.auth.getToken with the frob, and get
		# xml with the username, the token, and permissions.

		fapi = FlickrAPI(config['api_key'], config['api_secret'])

		frob = request.params.get('frob')
		if not frob:
			return "Invalid Response"

		rsp = fapi.auth_getToken(frob=frob)
		auth = rsp.find('auth')
		if not auth:
			return "invalid response from get token"
		
		username = auth.find('user').get('username').encode('ascii','ignore')
		token = auth.find('token').text
		nsid = auth.find('user').get('nsid')
		
		if not (username and token):
			return "Invalid Response from getToken"

		user = model.User.get_byNsid(nsid)
		if not user:
			user = model.User.get_byName(username)
			if not user:
				user = model.User()
				user.username = username
				user.nsid = auth.find('user').get('nsid')
				user.make_secret()
				user.save()
			user.nsid = nsid
			user.commit()
		else:
			# people can change usernames, nsids are static.
			if user.username != username:
				user.username=username
				user.commit()

		session['user'] = username
		session['nsid'] = nsid
		session['mod'] = user.check_mod(token)
		if session['mod']:
			session['token'] = token		
		session.save()

		# Send user back to the page he originally wanted to get to
		if session.get('path_before_login'):
			path = session['path_before_login']
			del(session['path_before_login'])
			redirect_to(path)
		else:
			if session.get('mod'):
				redirect_to('/ping/index')
			redirect_to('/profile/bookmarklet')
			
