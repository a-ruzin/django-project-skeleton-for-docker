from typing import Any

from django.urls import include, path, re_path, reverse
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from core.api.v1.views import (
    WorkspaceViewSet,
    UserInfoView,
)
from core.api.v1.views.jwt_views import CookieTokenObtainPairView, CookieTokenRefreshView, CookieTokenLogoutView
from core.api.v1.views.user_registration import (
    UserRegistrationRequestView,
    ConfirmRegistrationByCodeView,
    ConfirmRegistrationByTokenView,
)
from core.api.v1.views.version import VersionView

app_name = "core.api.v1"

"""
Настройка модуля drf-yasg (Yet another Swagger generator)
"""
api_info = openapi.Info(title="Mpass API", default_version="v1", description="Mpass API")

schema_view = get_schema_view(public=True, permission_classes=[permissions.AllowAny])

"""
Формирование маршрутов вида:
/api/v1/{class}/ - доступны GET, POST
/api/v1/{class}/pk/ - доступны GET, PUT, PATCH, DELETE

URLPatterns:
'^participant/$' [name='participant-list']
'^participant/(?P<pk>[^/.]+)/$' [name='participant-detail']
"""
# Основной роутер для workspaces
router = routers.SimpleRouter()
router.register(r'workspaces', WorkspaceViewSet)


class UnknownAPIURLRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Any:
        return reverse("core:api:v1:schema-swagger-ui")


urlpatterns = [
    path("", include(router.urls)),
    # JWT auth
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', CookieTokenLogoutView.as_view(), name='token_logout'),
    # swagger and docs
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(r"swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path(r"redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # user registration
    path("register/", UserRegistrationRequestView.as_view(), name="register-user"),

    path(
        f"register/<uuid:user_registration_id>/confirm/",
        ConfirmRegistrationByCodeView.as_view(),
        name="confirm-user-registration-by-code"
    ),
    path(
        f"register/<uuid:user_registration_id>/confirm/<uuid:token>/",
        ConfirmRegistrationByTokenView.as_view(),
        name="confirm-user-registration-by-token",
    ),

    # model viewsets
    path(r"user/", UserInfoView.as_view(), name="user"),
    path(r"version/", VersionView.as_view(), name="api_version"),
]
