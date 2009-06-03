from Orphereus.tests import *

class TestFcpController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='Orphereusp'))
        # Test response...
