from fmod.tests import *

class TestPingController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ping', action='index'))
        # Test response...
