from django.http import HttpResponse
from django.views.generic import TemplateView

from mapgen.utils import Map

class IndexView(TemplateView):
    template_name = 'display/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        default_map = Map()
        context['map_room'] = default_map.room
        context['map_seed'] = default_map.seed
        context['map_width'] = default_map.width
        context['map_height'] = default_map.height
        context['min_width'] = default_map.width * 11 + 1  # Eh...Template logic in View. Kinda gross.

        return context

