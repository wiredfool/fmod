import logging

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from fmod.lib.base import BaseController, render
from fmod import model
from sqlalchemy import desc

log = logging.getLogger(__name__)

import md5
import time, datetime

#useful for this case.
from fmod.model import Ping, ImageHistory
from flickrapi import FlickrAPI


class PingController(BaseController):

	def index(self):
		c.results=[]
		c.username = session.get('user')
		c.fl_mod = session.get('mod',False)
			
		images = {}
		flSave = False
		for ping in Ping.query().filter(Ping.fl_decided==False).order_by(Ping.id):
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
		
		filter_images = dict([(ping.image,True) for ping in
							  Ping.query().filter(Ping.fl_decided==False).filter(Ping.id<=pid)])

		for ping in Ping.query().filter(Ping.fl_decided==False).filter(Ping.id>pid).order_by(Ping.id):
			if not ping.image in filter_images:
				img = ping.Image_fromPing()
				if img.in_pool():
					c.ping=ping
					c.image=ping.image
					c.atts = img.all_atts()
					return render('one_ping.mako')
				else:
					ping.fl_decided=True
					ping.commit()

	def _fmtTime(self, t=None):
		if t!= None and hasattr(t, 'timetuple'):
			t = time.mktime(t.timetuple())
		return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(t))

	def rss(self):
		response.charset='utf8'
		response.headers['content-type'] = 'text/xml; charset=UTF-8'
		c.items=[]
		images = {}
		for ping in Ping.query().filter(Ping.fl_decided==False).order_by(desc(Ping.id)):
			if not images.get(ping.image):
				img = ping.Image_fromPing()
				if img.in_pool():
					images[ping.image] = True
					img.all_atts()
					c.items.append((ping,img))
					if len(c.results) >= 20:
						break

		c.fmtTime = self._fmtTime
		return render('rss.mako')


	def ping(self):
		log.debug('In Ping')
		params = {'nsid':'nsid',  # the pinging user, this is static. 
				  'uid':'username', # our userid
				  'id' :'image',  # image id
				  'own':'owner', # image owner
				  'sec':'secret', # image secret, from flickr
				  'con':'context', # context - in group pool
				  }
		#				  's':None	 # signature
		# check sig --

		nsid = request.params.get('nsid')
		if nsid:
			u = model.User.get_byNsid(nsid)
		else:
			u = model.User.get_byName(request.params.get('uid'))
		if not u:
			log.debug('user not found for ping: %s'%request.query_string)
			return ''

		
		log.debug(request.query_string)
		log.debug(request.query_string[:-35]+u.secret)
		log.debug(request.params.get('s'))
		log.debug(md5.new(request.query_string[:-35]+u.secret).hexdigest().lower()) 
		if md5.new(request.query_string[:-35]+u.secret).hexdigest().lower() != request.params.get('s'):
			log.debug('bad signature')
			return ''
		else:
			log.debug('good signature')

		p = Ping()
		for (arg, att) in params.items():
			# must filter!!!
			val = request.params.get(arg,'')
			log.debug("setting %s to %s"% (att, val))
			if val:
				setattr(p, att, val)
		p.username = u.username
		#p.begin()
		p.save()
		p.commit()

		if request.params.get('v',False) == '2':
			#version 2 response.
			response.headers['content-type'] = 'text/javascript'
			return """YUI().use('node', function(Y) {Y.one('#context-num-pool-71917374__at__N00').insert(document.createTextNode(' (Flagged) '), 'before')})"""
		else:
			#version 1 response
			"""	   q='uid='+uid+'&id='+p.id+'&own='+p.ownerNsid+'&sec='+p.secret+'&con='+nextprev_currentContextID;
			i.src='http://192.168.10.99:5000/p?'+q+'s='+md5_calcMD5(q+s);
			"""
			response.headers['content-type'] = 'text/javascript'
			return """Y.D.get('contextTitle_pool71917374@N00').appendChild(document.createTextNode('(Flagged)'))"""


	def dup_scan(self):
		log.debug('dup ping')
		fapi = FlickrAPI(config['api_key'], config['api_secret'])
		try:
			rsp = fapi.groups_pools_getPhotos(api_key=config['api_key'],
							  group_id=config['group_id'],
							  extras='last_update',
							  per_page='50',
							  page='1')
		except Exception,msg:
			log.debug(msg.args)
			return False
		photos = rsp.find('photos')
		for photo in photos.getchildren():
			image = photo.get('id')
			dt = int(photo.get('dateadded'))
			if ImageHistory.get(image=image, dt=dt):
				log.debug('found high water mark, quitting')
				break
			if ImageHistory.get_all(image=image):
				log.debug('found a re-add')
				p = Ping()
				p.image = image
				p.owner = photo.get('owner')
				p.reason = "Bump"
				p.username = 'RoboMod'
				p.save()
				Ping.commit()
				
			ih = ImageHistory()
			ih.image = image
			ih.dt = dt
			ih.save()
		ImageHistory.commit()
		return "successful"
