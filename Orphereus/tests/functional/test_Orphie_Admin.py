from Orphereus.tests import *

class TestOrphie_AdminController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller = 'Orphie_Admin'))
        # Test response...
