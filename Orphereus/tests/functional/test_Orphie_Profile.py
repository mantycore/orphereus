from Orphereus.tests import *

class TestOrphie_ProfileController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller = 'Orphie_Profile'))
        # Test response...
