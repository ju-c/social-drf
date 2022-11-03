from rest_framework.routers import DefaultRouter

from user_content.views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
