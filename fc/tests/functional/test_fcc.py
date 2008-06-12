from fc.tests import *

class TestFccController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='fcc'))
        # Test response...
