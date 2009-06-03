from Orphereus.tests import *

class TestFcaController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='Orphereusa'))
        # Test response...
