from fc.tests import *

class TestFcajaxController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='fcajax'))
        # Test response...
