from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.urls import router as user_router
from user_content.urls import router as user_content_router

app_name = "api"

urlpatterns = [
    path("auth/", include("users.urls", namespace="authentication")),
]

router = DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(user_content_router.registry)

urlpatterns += router.urls
