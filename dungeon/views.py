from django.http import HttpResponse
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'dungeon/index.html'

    # We'll eventually want to pay attention to the url to load specific maps
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = [[0, 1, 1],
                           [1, 0, 0],
                           [1, 1, 1]]
        return context
