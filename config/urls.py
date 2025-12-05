from django.contrib import admin
from django.urls import path, include
from workorders.views import AssetListView  

urlpatterns = [
    path("admin/", admin.site.urls),
    path("assets/", include("workorders.urls", namespace="assets")),
    path("", AssetListView.as_view(), name="home"),  #I've set the home page to the asset list view
]
