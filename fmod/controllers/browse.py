import logging

from pylons import config, request, response, session, url, tmpl_context as c
from pylons.controllers.util import abort, redirect

from fmod.lib.base import BaseController, render
from fmod import model
from sqlalchemy import desc

log = logging.getLogger(__name__)

import time, datetime
try:
    from elementtree import ElementTree as et
except:
    import xml.etree.ElementTree as et


from flickrapi import FlickrAPI

#useful for this case.
from fmod.model import Ping, PseudoPing, Decision, ImageHistory

class BrowseController(BaseController):

	def __before__(self):
		BaseController.__before__(self)
		# logged in...
		c.username = session.get('user', None)
		if not c.username or not session.get('mod',None):
			redirect(url('/flickr/login'))
		#if not request.method=='GET': #UNDONE POST
		#	throw("Error - must GET")

	def index(self):
		c.results=[]
		c.username = session.get('user')
		c.fl_mod = session.get('mod',False)
			
		images = {}
		flSave = False
		for ping in PseudoPing.query().filter(PseudoPing.fl_decided==False).order_by(PseudoPing.id):
			if not images.get(ping.image):
				img = ping.Image_fromPing()
				if img.in_pool():
					images[ping.image] = True
					c.results.append(ping)
					if len(c.results) >= 2:
						break
				else:
					flSave=True
					ping.fl_decided=True

		if not len(c.results):
			if self.reload():
				return self.index()
		
		if flSave: ping.commit()
		return render('ping.mako')

	def more(self, id=None):
		# id will be something like d_ping_[ping.id]
		# so, I want to get a ping where id > that one.
		pid = id.split('_')[-1]
		try:
			pid = int(pid)
		except:
			log.debug("couldn't identify the ping %s "%id)
			return ""

		c.username = session.get('user')
		c.fl_mod = session.get('mod',False)
		
		for ping in PseudoPing.query().filter(
			PseudoPing.fl_decided==False).filter(PseudoPing.id>pid).order_by(PseudoPing.id):
			img = ping.Image_fromPing()
			if img.in_pool():
				c.ping=ping
				c.image=ping.image
				c.atts = img.all_atts()
				return render('one_ping.mako')
			else:
				ping.fl_decided=True
				ping.commit()
		#Guess what. We're empty. get to bottom, go back to top. But this time, we need
		# to send back the newest image, rather than the next oldest one. 
		if not self._reload():
			return
		return self.more(id)

	def _reload(self):
		# Here, we grab some stuff from the pool, filter it against what we already have in the
		# db table, and make sure that we've got at least 20 items. 
		fapi = FlickrAPI(config['api_key'], config['api_secret'])
		bite_size = 20
		ct_checked = 0
		ct_added = 0
		ct_total = 200  # so long as this is > 0, we're ok.
		page = 1
		while ct_added < bite_size and ct_checked < ct_total:
			log.debug('downloading, starting at: %d' % ct_checked)
			try:
				rsp = fapi.groups_pools_getphotos(apikey=config['api_key'],
												  group_id=config['group_id'],
												  page=page,
												  per_page=100)
			except Exception, msg:
				log.debug(msg.args)
				return False
			
			log.debug(rsp)
			photos = rsp.find('photos')
			ct_checked += int(photos.get('perpage'))
			ct_total = int(photos.get('total'))
			log.debug('got photos %s'%photos)
			for photo in photos.getchildren():
				# photo_id, date_added == the tuple of a primary key. If it's there, then we skip it.
				image = photo.get('id')
				log.debug('checking %s'%image)
				dt = int(photo.get('dateadded'))
				if PseudoPing.get(image=image, dt=dt):
					log.debug('already in table')
					continue
				if Decision.get(image=image, fl_ok=True):
					log.debug('already decided good')
					continue
				if not ImageHistory.get(image=image, dt=dt):
					log.debug("adding image history entry, since one doesn't exist yet")
					#undone -- concurrency issue here?
					#undone -- check dup here?
					ih = ImageHistory()
					ih.image = image
					ih.dt = dt
					ih.save()
					ImageHistory.commit()
																	
				p = PseudoPing()
				p.image = image
				p.dt = dt
				p.owner = photo.get('owner')
				p.secret = photo.get('secret')
				log.debug('saving')
				ct_added += 1
				p.save()
				if ct_added >= bite_size:
					# thinking pulling just a small bite at a time would be better -- keep things fresher.
					# rather than sometimes pulling in 100 at a shot. 
					break
			page+=1
		log.debug('committing')
		PseudoPing.commit()
			
	def reload(self):
		self._reload()
		return "successful"


