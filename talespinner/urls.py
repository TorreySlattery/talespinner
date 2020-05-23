from django.contrib import admin
from django.urls import path, include

from frontend import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls"),),
    path("encounters/", views.EncountersView.as_view(), name="encounters_list"),
    path("encounters/<int:pk>/", views.EncountersView.as_view(), name="encounters_detail"),
    path("encounter-groups/", views.EncounterGroupsView.as_view(), name="encounter-groups_list"),
    path("encounter-groups/<int:pk>/", views.EncounterGroupsView.as_view(), name="encounter-groups_detail"),
]
