from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import CustomTokenObtainPairView, UserProfileViewSet

app_name = "user"

router = DefaultRouter()
router.register("user", UserProfileViewSet)

urlpatterns = [
    # TokenAuthentication endpoint to get token from login/password.
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
