from django.urls import path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# drf-yasg doc:
# https://drf-yasg.readthedocs.io/en/stable/readme.html#a-get-schema-view-parameters
# OpenAPI
# See: https://www.django-rest-framework.org/topics/documenting-your-api/
schema_view = get_schema_view(
    openapi.Info(
        title="Social Network API",
        default_version="v1",
        description="""Social Network API example""",
        terms_of_service="https://en.wikipedia.org/wiki/Terms_of_service",
        contact=openapi.Contact(email="julien.cortesi@protonmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    # Swagger-ui view of the API specification
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
