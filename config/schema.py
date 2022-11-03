from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
import os


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.basePath = "/" + os.environ.get("REDIRECT_PREFIX", "api")
        return schema


def get_custom_schema_view():
    return get_schema_view(
        openapi.Info(
            title="Social Network DRF API",
            default_version="v1",
            description="""Social Network DRF API example""",
            terms_of_service="https://en.wikipedia.org/wiki/Terms_of_service",
            contact=openapi.Contact(email="julien.cortesi@protonmail.com"),
            license=openapi.License(name="MIT"),
        ),
        url="https://julienc.net",
        public=True,
        permission_classes=[AllowAny],
        generator_class=SchemaGenerator,
    )
