from django.views.generic.base import TemplateView

"""
In general, the idea here is to treat the frontend as if it were an external client that has to consume the 
endpoint response like anyone else would.  
"""


class EncounterView(TemplateView):
    template_name = "frontend/encounters.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data()