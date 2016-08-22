from django.http import HttpResponse
from django.views.generic import TemplateView

from mapgen.utils import Map

class IndexView(TemplateView):
    template_name = 'display/index.html'

    def get_room(self):
        """
        Seeing how this feels. Is it a neat trick, or a bad idea to call it directly from the template?
        """
        default_map = Map()
        return default_map.room
