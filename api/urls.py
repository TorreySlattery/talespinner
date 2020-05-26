from django.urls import include, path

from rest_framework.routers import DefaultRouter

import api.views

router = DefaultRouter()
router.register("encounters", api.views.EncounterViewSet)
router.register("encounter-groups", api.views.EncounterGroupViewSet),

urlpatterns = [
    path("", include(router.urls)),
    path("roll/", api.views.RollView.as_view(), name="roll"),
]
