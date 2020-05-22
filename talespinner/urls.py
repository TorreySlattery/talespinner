from django.contrib import admin
from django.urls import path, include

from frontend.views import EncounterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls"),),
    path("encounters/", EncounterView.as_view(), name="encounters_list"),
    path("encounters/<int:pk>/", EncounterView.as_view(), name="encounters_detail")
]
