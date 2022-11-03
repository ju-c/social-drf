from django.urls import path
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    # See: https://www.django-rest-framework.org/topics/documenting-your-api/
    path("", include_docs_urls(title="Social Network API")),
]
