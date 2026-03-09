from django.urls import include, path

app_name = "core.api"

urlpatterns = [path("v1/", include("core.api.v1.urls", namespace="v1"))]
