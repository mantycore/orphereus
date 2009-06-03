from Orphereus.tests import *

class TestOrphieAjaxController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller = 'OrphieAjax'))
        # Test response...
