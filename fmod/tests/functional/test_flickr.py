from fmod.tests import *

class TestFlickrController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='flickr', action='index'))
        # Test response...
