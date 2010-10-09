from fmod.tests import *

class TestModerateController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='moderate', action='index'))
        # Test response...
