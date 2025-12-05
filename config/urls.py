from django.contrib import admin
from django.urls import path, include
from workorders.views import AssetListView  # import your list view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("assets/", include("workorders.urls", namespace="assets")),
    path("", AssetListView.as_view(), name="home"),  # root path shows asset list
]
