from Orphereus.tests import *

class TestOrphie_AjaxController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller = 'Orphie_Ajax'))
        # Test response...
