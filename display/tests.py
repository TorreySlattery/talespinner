from django.test import TestCase
from django.core.urlresolvers import reverse

from display.views import IndexView

class IndexViewTestCase(TestCase):

    def test_smoke_test(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # We'll add more meaningful tests as the view and template get fleshed out
