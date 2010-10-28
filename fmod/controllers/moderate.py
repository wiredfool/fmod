import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from fmod.lib.base import BaseController, render
from fmod import model

log = logging.getLogger(__name__)

class ModerateController(BaseController):

	requires_auth=True
	
	def __before__(self):
		BaseController.__before__(self)
		# logged in...
		c.username = session['user']
		if not session['mod']:
			redirect_to('/ping/index')
		#if not request.method=='GET': #UNDONE POST
		#	throw("Error - must GET")

	def _get_decision(self, id, flag):
		if id == None:
			raise "Error - Need an image id"
		d = model.Decision()
		setattr(d, flag, True)
		d.image = id
		d.username = c.username
		d.save()
		d.update_pings()
		d.commit()
		return d

	def _remove(self, d, tag, rule=None):
		img = d.getImage()
		if img.in_pool():
			tags = [tag, 'removed-from-strobist-pool']
			if rule:
				tags.append('see-rule-%s'%rule)
			img.tag(tags, session['token'])
			ret = img.remove_from_group(session['token'])
			if ret:
				return "Success"
			else:
				return "Could not remove from pool"
		else:
			return "Not in pool"

	def defer(self, id=None):
		#this is a noop. 
		return "Success"
			
	def ok(self, id=None):
		try:
			self._get_decision(id, 'fl_ok')
			return "Success"
		except Exception, msg:
			return msg
	
	def ns(self, id=None):
		try:
			d = self._get_decision(id, 'fl_ns')
			return self._remove(d, 'no-off-camera-flash',1)
		except Exception, msg:
			return msg

	def nsi(self, id=None):
		try:
			d = self._get_decision(id, 'fl_nsi')
			return self._remove(d, 'no-strobist-info',2)
		except Exception, msg:
			return msg

	def isi(self, id=None):
		try:
			d = self._get_decision(id, 'fl_isi')
			return self._remove(d, 'incomplete-strobist-info',2)
		except Exception, msg:
			return msg
		
	def nsfw(self, id=None):
		try:
			d = self._get_decision(id, 'fl_nsfw')
			return self._remove(d, 'NSFW',3)
		except Exception, msg:
			return msg

	def bump(self, id=None):
		try:
			d = self._get_decision(id, 'fl_bump')
			return self._remove(d, 'no-bumping')
		except Exception, msg:
			return msg



		
