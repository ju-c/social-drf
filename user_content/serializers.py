from rest_framework import serializers

from users.serializers import UserSerializer
from user_content.models import Like, Post, Comment


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = "__all__"


class LikeUnlikeSerializer(serializers.Serializer):
    LIKEUNLIKE = (
        ("LIKE", "like"),
        ("UNLIKE", "unlike"),
    )

    action = serializers.ChoiceField(
        choices=LIKEUNLIKE,
        error_messages={"invalid_choice": "The request action is not valid."},
    )
    post = serializers.CharField(
        max_length=255,
        required=False,
        error_messages={"max_length": "The post is too Long (max: 255)."},
    )


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreationSerializer(serializers.ModelSerializer):
    # HiddenField doc:
    # https://www.django-rest-framework.org/api-guide/fields/#hiddenfield
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    # SerializerMethodField doc:
    # https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    likes_count = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()
    likes = LikeSerializer(source="like_set", many=True, read_only=True)
    comments = CommentSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Post
        fields = "__all__"

    @staticmethod
    def get_likes_count(self):
        return self.likes.count()

    @staticmethod
    def get_reposts_count(self):
        return self.reposts.count()


class PostCreationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    content = serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = (
            "user",
            "content",
            "image",
            "video",
            "created_at",
            "parent_content",
            "comment",
            "image",
            "video",
        )
        extra_kwargs = {
            "content": {"error_messages": {"max_length": "max: 255 chars."}}
        }

    def validate(self, data):
        if "content" not in data:
            if "parent_content" not in data or "comment" not in data:
                raise serializers.ValidationError({"message": "Content is necessary"})

        if "parent_content" in data and "comment" in data:
            raise serializers.ValidationError(
                {"message": "Repost only can related to a post or comment, not both"}
            )

        return data
