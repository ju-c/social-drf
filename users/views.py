# More infos on get_user_model: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#django.contrib.auth.get_user_model
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
# More infos on DRF's parsers: https://www.django-rest-framework.org/api-guide/parsers/
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import (
    CustomTokenObtainPairSerializer,
    RegisteringUserSerializer,
    UserSerializer,
)
from utils.permissions import IsOriginalUserOrReadOnly


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOriginalUserOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = "uuid"

    def get_permissions(self):
        if self.action in ["create"]:
            return [
                AllowAny(),
            ]
        return super(UserProfileViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        register_serializer = RegisteringUserSerializer(data=request.data)
        if register_serializer.is_valid():
            new_user = register_serializer.save()
            if new_user:
                return Response(
                    register_serializer.data, status=status.HTTP_201_CREATED
                )

        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        current_user = self.get_object()
        if "action" in request.data:
            action = request.data["action"]
            if "follow_uuid" in request.data:
                user_to_perform_action = get_user_model().objects.get(
                    uuid=request.data["follow_uuid"]
                )
                if action == "FOLLOW":
                    if user_to_perform_action in current_user.following.all():
                        return Response(
                            {"message": "The user has already been followed"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    current_user.following.add(user_to_perform_action)

                elif action == "UNFOLLOW":
                    if user_to_perform_action not in current_user.following.all():
                        return Response(
                            {"message": "The user is not yet followed"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    current_user.following.remove(user_to_perform_action)

        user_serializer = UserSerializer(
            data=request.data,
            instance=current_user,
            partial=True,
            context={"request": request},
        )

        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def get_parsers(self):
        """
        Put this if Error with swagger appear - parsers problem
        :return:
        :rtype:
        """
        if getattr(self, "swagger_fake_view", False):
            return []

        return super().get_parsers()
