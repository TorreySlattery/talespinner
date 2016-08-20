from django.http import HttpResponse
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'dungeon/index.html'

    # We'll eventually want to pay attention to the url to load specific maps
