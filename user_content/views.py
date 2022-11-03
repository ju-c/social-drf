from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from user_content.models import Post, Comment
from user_content.serializers import (
    LikeUnlikeSerializer,
    CommentSerializer,
    CommentCreationSerializer,
    PostSerializer,
    PostCreationSerializer,
)
from utils.permissions import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for viewing comments.
    """

    permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    serializer_class_create = CommentCreationSerializer
    # MultiPartParser & FormParser doc:
    # https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
    parser_classes = [MultiPartParser, FormParser]

    # Overriding the get_serializer_class method.
    # This method is used in the model mixins to
    # retrieve the proper Serializer class.
    def get_serializer_class(self):
        if self.action == "create":
            return self.serializer_class_create
        return self.serializer_class

    def get_parsers(self):
        # Representing arrays of files is not doable with OpenAPI 2.0.
        # Using swagger_fake_view will render the files field as read-only.
        # swagger_fake_view doc:
        # https://drf-yasg.readthedocs.io/en/stable/openapi.html#a-note-on-limitations
        if getattr(self, "swagger_fake_view", False):
            return []

        return super().get_parsers()


class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset for viewing and editing posts.
    """

    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    serializer_class_create = PostCreationSerializer
    # MultiPaartParser & FormParser doc:
    # https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
    parser_classes = [MultiPartParser, FormParser]

    def partial_update(self, request, *args, **kwargs):
        current_post = self.get_object()
        if "action" in request.data:
            action_serializer = LikeUnlikeSerializer(data=request.data)
            if not action_serializer.is_valid():
                return Response(action_serializer.errors, status.HTTP_400_BAD_REQUEST)
            action = action_serializer.data.get("action")
            if action == "LIKE":
                current_post.likes.add(request.user)
            if action == "UNLIKE":
                current_post.likes.remove(request.user)

        post_serializer = PostSerializer(
            data=request.data,
            instance=current_post,
            partial=True,
            context={"request", request},
        )
        if not post_serializer.is_valid():
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        post_serializer.save()
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    # Overriding the get_serializer_class method.
    # This method is used in the model mixins to
    # retrieve the proper Serializer class.
    def get_serializer_class(self):
        if self.action == "create":
            return self.serializer_class_create
        return self.serializer_class

    def get_queryset(self):
        if self.action == "list":
            user_id = self.request.query_params.get("user_id", None)
            if user_id:
                return Post.objects.filter(user__uuid=user_id)
        return Post.objects.all()

    def get_parsers(self):
        # Representing arrays of files is not doable with OpenAPI 2.0.
        # Using swagger_fake_view will render the files field as read-only.
        # swagger_fake_view doc:
        # https://drf-yasg.readthedocs.io/en/stable/openapi.html#a-note-on-limitations

        if getattr(self, "swagger_fake_view", False):
            return []

        return super().get_parsers()
