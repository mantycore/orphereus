from Orphereus.tests import *

class TestOrphie_PublicController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller = 'Orphie_Public'))
        # Test response...
