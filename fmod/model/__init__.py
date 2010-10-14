"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from fmod.model import meta
import logging
log = logging.getLogger(__name__)
import md5, random
try:
    from elementtree import ElementTree as et
except:
    import xml.etree.ElementTree as et

import time

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)

    sm = orm.sessionmaker(autoflush=True,
						  autocommit=False,
						  bind=engine,
						  expire_on_commit=False)

    meta.engine = engine
    meta.Session = orm.scoped_session(sm)

class base_orm(object):
	# cause this model.meta.Session.* crap in my controllers blows.
	@classmethod
	def query(cls):
		return meta.Session.query(cls)
	def save(self):
		meta.Session.save(self)
	def flush(self):
		meta.Session.flush(self)
	@staticmethod
	def begin():
		meta.Session.begin()
	@staticmethod
	def commit():
		meta.Session.commit()
	@classmethod
	def get(cls, **kwargs):
		try:
			return cls.query().filter_by(**kwargs).one()
		except Exception,msg:
			# either not found, or only one item.
			return None
	@classmethod
	def get_all(cls, **kwargs):
		return cls.query().filter_by(**kwargs).all()

		

t_pings = sa.Table("pings", meta.metadata,
				   sa.Column("id", sa.types.Integer, primary_key=True),
				   sa.Column("image", sa.types.Text, primary_key=False),
				   sa.Column("owner", sa.types.Text, primary_key=False),
				   sa.Column("username", sa.types.Text, primary_key=False),
				   sa.Column("secret", sa.types.Text, primary_key=False),
				   sa.Column("context", sa.types.Text, primary_key=False),
				   sa.Column("dt", sa.types.DateTime(timezone=True), primary_key=False, default=sa.func.now()),
				   sa.Column("fl_decided", sa.types.Boolean, primary_key=False, default=False), # has it been modded 
				   sa.Column("reason", sa.types.Text, primary_key=False, default='Ping'),
				   sa.Column("nsid", sa.types.Text, primary_key=False),
				   )

class Ping(base_orm):
	def Image_fromPing(self):
		image = Image.get_byId(self.image)
		if image:
			return image
		image = Image()
		image.image = self.image
		image.owner = self.owner
		image.secret = self.secret
		image.save()
		image.commit()
		return image
	
orm.mapper(Ping, t_pings)

class PseudoPing(Ping): pass 
t_pseudopings = sa.Table("pseudopings", meta.metadata,
				   sa.Column("id", sa.types.Integer, primary_key=True),
				   sa.Column("image", sa.types.Text, primary_key=False),
				   sa.Column("owner", sa.types.Text, primary_key=False),
				   sa.Column("username", sa.types.Text, primary_key=False),
				   sa.Column("secret", sa.types.Text, primary_key=False),
				   sa.Column("context", sa.types.Text, primary_key=False),
				   sa.Column("dt", sa.types.Integer, primary_key=False),
				   sa.Column("fl_decided", sa.types.Boolean, primary_key=False, default=False), # has it been modded 
				   sa.Column("reason", sa.types.Text, primary_key=False, default='Ping'),
				   sa.Column("nsid", sa.types.Text, primary_key=False),
				   )
orm.mapper(PseudoPing, t_pseudopings)

class Decision(base_orm):
	def update_pings(self):
		for ping in Ping.get_all(image=self.image):
			ping.fl_decided=True
		for ping in PseudoPing.get_all(image=self.image):
			ping.fl_decided=True			
			
	def getImage(self):
		image = Image.get_byId(self.image)
		if image:
			return image
		log.warn("We should never be in here - decision on an image %s that's not in the db" % self.image)
		return None
		
t_decisions = sa.Table('decisions', meta.metadata,
					   sa.Column("id", sa.types.Integer, primary_key=True),
					   sa.Column("image", sa.types.Text, primary_key=False),
					   sa.Column("username", sa.types.Text, primary_key=False),
					   sa.Column("fl_ok", sa.types.Boolean, primary_key=False), # ok
					   sa.Column("fl_nsfw", sa.types.Boolean, primary_key=False), # not safe for work
					   sa.Column("fl_ns", sa.types.Boolean, primary_key=False), # not strobist
					   sa.Column("fl_nsi", sa.types.Boolean, primary_key=False), # no strobist info
					   sa.Column("fl_isi", sa.types.Boolean, primary_key=False), # incomplete strobist info
					   sa.Column("dt", sa.types.DateTime(timezone=True), primary_key=False, default=sa.func.now()),
					   )
orm.mapper(Decision, t_decisions)


t_imagehistory = sa.Table('imagehistory', meta.metadata,                       
                       sa.Column("image", sa.types.Text, primary_key=True),
                       sa.Column("dt", sa.types.Integer, primary_key=True),)

class ImageHistory(base_orm):
    pass

orm.mapper(ImageHistory, t_imagehistory)


t_users = sa.Table("users", meta.metadata,
				   sa.Column("username", sa.types.Text, primary_key=True),
				   sa.Column("secret", sa.types.Text, primary_key=False),
				   sa.Column("password", sa.types.Text, primary_key=False),
				   sa.Column("admin", sa.types.Boolean, primary_key=False),
				   sa.Column("nsid", sa.types.Boolean, primary_key=False),
)

class User(base_orm):
	@classmethod
	def get_byName(cls, name):
		return cls.get(username=name)
	@classmethod
	def get_byNsid(cls, id):
		return cls.get(nsid=id)

	def make_secret(self):
		#not totally secure, but good enough
		self.secret = md5.md5(str(random.random())).hexdigest()[:8]

	def check_mod(self, token):
		def cb():
			fapi = FlickrAPI(config['api_key'], config['api_secret'], token=token)
			rsp = fapi.groups_members_getList(group_id=config['group_id'],
											  membertypes='3,4', # moderators, admin
											  )
			log.debug(et.tostring(rsp))
			members = rsp.find('members')
			return [member.get('username') for member in members]

		log.debug('checking mod, %s' % self.username)

		mods = mc_flickr('strobist', 'mods', 1440*60).get(cb)
		log.debug('mods: %s' %mods)
		
		if self.username in mods:
			return True
		return False

	def set_password(self, password):
		self.password = md5.md5(password).hexdigest()

	def check_password(self, password):
		return self.password and self.password == md5.md5(password).hexdigest()

		
orm.mapper(User, t_users)

t_images = sa.Table("images", meta.metadata,
				   sa.Column("image", sa.types.Text, primary_key=True),
				   sa.Column("owner", sa.types.Text, primary_key=False),
				   sa.Column("secret", sa.types.Text, primary_key=False),
				   sa.Column("image_url", sa.types.Text, primary_key=False),
				   sa.Column("photo_url", sa.types.Text, primary_key=False),
				   )


from pylons import config, session, request
from flickrapi import FlickrAPI
import memcache
import Queue
from threading import Thread

class worker(Thread):
	def __init__(self, cb):
		Thread.__init__(self)
		self.cb = cb
		self.start()
	def run(self): self.cb()

class _mc_pool:
	def __init__(self):
		self.queue = Queue.Queue()
	def get(self):
		try:
			log.debug('Getting memcache obj')
			log.debug('Queue Length: %s'% self.queue.qsize())
			return self.queue.get_nowait()
		except Exception, msg:
			log.debug('exception getting memcache obj, returning new one: %s'%msg)
			return memcache.Client([config['memcached_url']], debug=0)
		
	def release(self, connection):
		log.debug('releasing memcache obj')
		self.queue.put(connection)
		log.debug('Queue Length: %s'% self.queue.qsize())

mc_pool = _mc_pool()

class mc_flickr:
	def __init__(self, img, op, timeout=5*60):
		self.img = img
		self.op = op
		self.timeout = timeout
		
	def get(self, cb, *args, **kwargs):
		mc = mc_pool.get()
		val = mc.get(self._key())
		if val:
			mc_pool.release(mc)
			return val
		val = cb(*args, **kwargs)
		mc.set(self._key(), val, self.timeout)
		mc_pool.release(mc)
		return val

	def _key(self):
		return str("%s_%s_%s" %("fm", self.img, self.op))


class Image(base_orm):
## 	t_images = sa.Table("images", meta.metadata,
## 						sa.Column("image", sa.types.Text, primary_key=True),
## 						sa.Column("owner", sa.types.Text, primary_key=False),
## 						sa.Column("secret", sa.types.Text, primary_key=False),
## 						)

	@classmethod
	def get_byId(cls, name):
		return cls.get(image=name)

	def _setup_atts(self):
		if not hasattr(self, 'atts'):
			self.atts = {}

	def getImages_forOwner(self):
		return Image.get_all(owner=self.owner)
	
	def getPings(self):
		return Ping.get_all(image=self.image)
		
	def getPings_forOwner(self):
		return Ping.get_all(owner=self.owner)

	def getDecisions(self):
		return Decision.get_all(image=self.image)

	def getDecisions_forOwner(self):
		# join, not easy.
		pass

	def getHistory(self):
		return ImageHistory.get_all(image=self.image)

	def all_atts(self):
		self._setup_atts()
		#kickoff
		workers = [worker(getattr(self,method)) for method in ['in_pool',
															   'owner_comments',
															   'info']]
		decisions = self.getDecisions()
		history = self.getHistory()
		self.atts['ctNsi'] = sum([1 for d in decisions if d.fl_nsi])
		self.atts['ctOk'] = sum([1 for d in decisions if d.fl_ok])
		self.atts['history'] = [time.strftime('%X %x', time.gmtime(h.dt)) for h in history]
		self.atts['ctHistory'] = len(history)
		self.atts['ctDecisions'] = len(decisions)
		# wait for them all to finish		
		[w.isAlive() and w.join() for w in workers]
		if hasattr(self, 'fl_dirty') and self.fl_dirty:
			self.commit()
			
		return self.atts

	def tag(self, tags, token):
		fapi = FlickrAPI(config['api_key'], config['api_secret'], token=token)
		if type(tags) == type([]):
			tags = ','.join(tags)
		try:
			rsp = fapi.photos_addTags(photo_id=self.image,
									  tags=tags)
		except Exception, msg:
			log.debug('Exception adding tags (%s) to %s: %s' %(tags, self.image, msg))
			return False
		return True

	def remove_from_group(self, token):
		fapi = FlickrAPI(config['api_key'], config['api_secret'], token=token)
		try:
			rsp = fapi.groups_pools_remove(photo_id=self.image,
										   group_id=config['group_id'])
		except Exception, msg:
			log.debug('Exception removing from group: %s' %(msg))
			return False
		return True

	def in_pool(self):
		# returns True/False/None for Yes, No, Error
		self._setup_atts()
		if 'in-pool' in self.atts: return self.atts['in-pool']
		
		def cb():
			fapi = FlickrAPI(config['api_key'], config['api_secret'])
			try:
				rsp = fapi.groups_pools_getContext(apikey=config['api_key'],
												   photo_id=self.image,
												   group_id=config['group_id'])
			except Exception, msg:
				log.debug(msg.args)
				if ": 2:" in msg.args[0]:
					return {'in-pool':False}
				return {}
			else:
				return {'in-pool': True}
			
		res = mc_flickr(self.image, 'in_pool', timeout=1*60).get(cb)
		log.debug(dir(self))
		self.atts['in-pool'] = res.get('in-pool', None)
		return self.atts['in-pool']
		
	def owner_comments(self):
		self._setup_atts()
		if 'comments' in self.atts: return self.atts['comments']
		
		def cb():
			fapi = FlickrAPI(config['api_key'], config['api_secret'])
			try:
				rsp = fapi.photos_comments_getList(apikey=config['api_key'],
												   photo_id=self.image
												   )
			except Exception,msg:
				log.debug("Exception getting comments: %s" %msg)
				return {}

			comments = rsp.find('comments')
			ret = {'comments':[]}
			for comment in comments:
				if comment.get('author') == self.owner:
					ret['comments'].append(comment.text)					
			return ret

		ret = mc_flickr(self.image, 'comments').get(cb)
		self.atts['comments'] = ret.get('comments','')
		return self.atts['comments']

	def info(self):
		self._setup_atts()
		if 'title' in self.atts: return self.atts
		
		def cb():
			self.fl_dirty = False
			fapi = FlickrAPI(config['api_key'], config['api_secret'])
			try:
				rsp = fapi.photos_getInfo(apikey=config['api_key'],
										  photo_id=self.image,
										  secret=self.secret)
			except Exception,msg:
				log.debug("Exception getting image info: %s" %msg)
				return {}

			photo = rsp.find('photo')
			ret = {}
			ret['img_url'] =  "http://farm%s.static.flickr.com/%s/%s_%s_m.jpg" % (
				photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
			if self.image_url != ret['img_url']:
				self.image_url = ret['img_url']
				log.debug(self.image_url)
				log.debug('set image url')
				self.fl_dirty=True
			ret['title'] = photo.find('title').text
			ret['description'] = photo.find('description').text or ' '
			for (ent,ch) in [('&quot;','"'), ('&lt;','<'),('&gt;','>'),('&amp;','&'),('\n\n','<br />')]:
				ret['description'] = ret['description'].replace(ent,ch) 
			log.debug('description %s'% ret['description'])
			ret['tags'] = []
			for tag in photo.find('tags'):
				if tag.get('author') == self.owner:
					ret['tags'].append(tag.get('raw'))
			ret['notes'] = []
			for note in photo.find('notes'):
				if note.get('author') == self.owner:
					ret['notes'].append(note.text)
			for url in photo.find('urls'):
				if url.get('type')=='photopage':
					ret['photo_url'] = url.text
					if self.photo_url != url.text:
						self.photo_url = url.text
						log.debug(self.photo_url)
						log.debug('set photo url')
						self.fl_dirty = True
			ret['username'] = photo.find('owner').get('username')
			ret['owner'] = self.owner
			return ret

		ret = mc_flickr(self.image, 'info').get(cb)
		for (k,v) in ret.items():
			self.atts[k]=v
		return ret

# see class model.image.Image
orm.mapper(Image, t_images)



## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
