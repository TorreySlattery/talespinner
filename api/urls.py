from django.urls import include, path

from rest_framework.routers import DefaultRouter

import api.views

router = DefaultRouter()
router.register("encounters", api.views.EncounterViewSet)

urlpatterns = [path("", include(router.urls))]
