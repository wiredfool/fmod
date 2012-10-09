"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
	"""Create, configure and return the routes Mapper"""
	map = Mapper(directory=config['pylons.paths']['controllers'],
				 always_scan=config['debug'])
	map.minimization = False
	
	# The ErrorController route (handles 404/500 error pages); it should
	# likely stay at the top, ensuring it can always be resolved
	map.connect('/error/{action}', controller='error')
	map.connect('/error/{action}/{id}', controller='error')

	# CUSTOM ROUTES HERE

	map.connect('/{controller}/{action}/{id}')
	map.connect('/{controller}/{action}')
	map.connect('/{controller}s', action='index') # added 
	map.connect('/{controller}', action='index') # added

	map.connect('/debug', controller='hello', action='index')  # added
	map.connect('/p', controller='ping', action='ping')	 # added
	map.connect('/logout', controller='login', action='logout')	 # added
	map.connect('/', controller='hello', action='home')	 # added


	return map
