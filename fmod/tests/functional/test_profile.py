from fmod.tests import *

class TestProfileController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='profile', action='index'))
        # Test response...
