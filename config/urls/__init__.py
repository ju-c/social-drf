from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # Admin urls
    path("admin/", include("config.urls.admin")),
    # API urls
    path("api/v1/", include("api.urls", namespace="api")),
    # API docs urls
    path("api/v1/docs/", include("config.urls.documentation")),
    # API Specification urls
    path("api/v1/swagger/", include("config.urls.swagger")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
