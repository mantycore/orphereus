from Orphereus.tests import *

class TestOrphie_MainController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller = 'Orphie_Main'))
        # Test response...
