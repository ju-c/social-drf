from django.urls import path, include

urlpatterns = [
    # API urls using the api apps urls
    path("api/v1/", include("api.urls", namespace="api")),
]
