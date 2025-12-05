from django.urls import path
from . import views

app_name = "assets"

urlpatterns = [
    path("", views.AssetListView.as_view(), name="list"),
    path("create/", views.AssetCreateView.as_view(), name="create"),
    path("<int:pk>/", views.AssetDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.AssetUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.AssetDeleteView.as_view(), name="delete"),
    path("<int:pk>/toggle-in-use/", views.toggle_in_use, name="toggle_in_use"),
]
