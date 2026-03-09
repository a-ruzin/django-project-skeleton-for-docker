from django.urls import path, re_path, include

from core.views import IndexView

app_name = 'core'
urlpatterns = (
    [
        path("api/", include("core.api.urls", namespace="api")),
        path('', IndexView.as_view(), name='index'),
        path("login/", IndexView.as_view(), name="login"),
        re_path("^.*$", IndexView.as_view()),
    ]
)
