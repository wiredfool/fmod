import logging

from pylons import request, response, session, tmpl_context as c, config
from pylons.controllers.util import abort, redirect_to

from fmod.lib.base import BaseController, render
from fmod import model

log = logging.getLogger(__name__)


class ImageController(BaseController):

	def _requireImg(self, id ):
		img = model.Image.get_byId(id)
		if not img:
			ping = model.Ping.get(image=id)
			if ping:
				img = ping.Image_fromPing()
			if not img:
				return None
		return img
		

	def view(self, id=None):
		if id == None: return "Image id required"
		img = self._requireImg(id)
		if not img:	return "Image not found"

		c.atts = img.all_atts()
			
		return render('image_view.mako')
		
	def all_atts(self, id=None):
		if id == None: return "Image id required"
		img = self._requireImg(id)
		if not img:	return "Image not found"

		atts = img.all_atts()
			
		return str(atts)

	def info(self, id=None):
		if id == None: return "Image id required"
		img = self._requireImg(id)
		if not img:	return "Image not found"

		ret = img.info()
			
		return str(ret)
		
	def in_pool(self, id=None):
		if id == None: return "Image id required"
		img = self._requireImg(id)
		if not img:	return "Image not found"

		ret = img.in_pool()
		#json for now
		return str({'in-pool':ret}) 

	def owner_comments(self, id=None):
		if id == None: return "Image id required"
		img = self._requireImg(id)
		if not img:	return "Image not found"
			
		ret = img.owner_comments()
		#json for now
		return str({'comments':ret})
