from builtins import staticmethod

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html#customizing-token-claims
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class FollowAndFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "avatar")


class UserSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followers = FollowAndFollowersSerializer(many=True)
    following = FollowAndFollowersSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = (
            "uuid",
            "username",
            "first_name",
            "last_name",
            "biography",
            "current_activity",
            "location",
            "date_of_birth",
            "avatar",
            "cover_picture",
            "verified_account",
            "date_joined",
            "following",
            "following_count",
            "followers",
            "followers_count",
        )

    @staticmethod
    def get_following_count(self):
        return self.following.count()

    @staticmethod
    def get_followers_count(self):
        return self.followers.count()


class RegisteringUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password"
    )

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="This email is already in use.",
            )
        ]
    )

    class Meta:
        model = get_user_model()
        fields = [
            "uuid",
            "username",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "biography",
            "current_activity",
            "location",
            "date_of_birth",
            "avatar",
            "cover_picture",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "uuid": {"read_only": True},
        }

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "Error: The passwords didn't match"}
            )

        return attrs

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        first_name = validated_data["first_name"] if "first_name" in validated_data else None
        last_name = validated_data["last_name"] if "last_name" in validated_data else None
        biography = validated_data["biography"] if "biography" in validated_data else None
        current_activity = validated_data["current_activity"] if "current_activity" in validated_data else None
        location = validated_data["location"] if "location" in validated_data else None
        date_of_birth = validated_data["date_of_birth"] if "date_of_birth" in validated_data else None
        avatar = validated_data["avatar"] if "avatar" in validated_data else None
        cover_picture = (
            validated_data["cover_picture"]
            if "cover_picture" in validated_data
            else None
        )

        user = self.Meta.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            biography=biography,
            current_activity=current_activity,
            location=location,
            date_of_birth=date_of_birth,
            avatar=avatar,
            cover_picture=cover_picture,
        )
        user.set_password(password)
        user.save()
        return user
