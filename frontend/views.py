import json

import requests

from django.views.generic.base import TemplateView
from django.shortcuts import render

from talespinner import constants

"""
In general, the idea here is to treat the frontend as if it were an external client that has to consume the
endpoint response like anyone else would, so no reverse() calls to the api urls or direct model access, etc.
"""


class EncounterView(TemplateView):
    template_name = "frontend/encounters.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        encounter_id = context.get("pk", None)
        url = f"{constants.TALESPINNER_BASE_URL}{constants.TALESPINNER_ENCOUNTER_URL}"
        if encounter_id:
            url = f"{url}{encounter_id}"

        response = requests.get(url)
        data = response.json()
        context["encounters"] = data

        return render(request, self.template_name, context)
