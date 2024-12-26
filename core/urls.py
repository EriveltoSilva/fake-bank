""" Global url project """

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title=f"{settings.APPLICATION_NAME} API",
        default_version="v1",
        description=f"{settings.APPLICATION_NAME} descrição",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=settings.EMAIL_HOST_USER),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("apps.accounts.urls")),
    path("api/v1/bank/", include("apps.bank.urls")),
    # Installed apps urls
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("api/v1/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
