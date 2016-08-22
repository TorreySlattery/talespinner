from django.test import TestCase

from display.views import IndexView

class IndexViewTestCase(TestCase):

    def test_smoke_test(self):
        response = self.client.get(reverse('display:index'))
        self.assertEqual(response.status_code, 200)

    # We'll add more meaningful tests as the view and template get fleshed out
