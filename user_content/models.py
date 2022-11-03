from django.conf import settings
from django.db import models

# gettext_lazy will translate the string to the activated
# language if we defined a translation.
# See: https://docs.djangoproject.com/en/4.1/topics/i18n/translation/
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    user = models.ForeignKey(
        User,
        related_name="posts",
        on_delete=models.CASCADE,
        help_text=_("Designates the post creator."),
    )
    content = models.CharField(
        max_length=300,
        help_text=_("Designates the post content (text)"),
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="user_content_images",
        help_text=_("Designates the post content (image)"),
    )
    video = models.FileField(
        blank=True,
        null=True,
        upload_to="user_content_videos",
        help_text=_("Designates the post content (video)"),
    )
    likes = models.ManyToManyField(
        User,
        blank=True,
        through=Like,
        related_name="post",
        help_text=_("Designates the post's likes"),
    )
    # Self-referencing foreign key used to
    # model recursive relationships
    # (an object that has a many-to-one
    # relationship with itself)
    parent_content = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL,
        related_name="reposts",
        help_text=_("Designates the reposts"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Designates the post creation date."),
    )
    comment = models.ForeignKey(
        "Comment",
        null=True,
        on_delete=models.CASCADE,
        related_name="reposts",
        help_text=_("Designates the post comments."),
    )

    def __str__(self):
        return self.content


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
        help_text=_("Designates the comment creator"),
    )
    content = models.CharField(
        max_length=255,
        help_text=_("Designates the comment content (text)"),
    )
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
        help_text=_("Designates the commented post."),
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="user_content_images",
        help_text=_("Designates the comment content (image)"),
    )
    video = models.FileField(
        blank=True,
        null=True,
        upload_to="user_content_videos",
        help_text=_("Designates the comment content (video)"),
    )
    likes = models.ManyToManyField(
        User,
        related_name="comment",
        blank=True,
        help_text=_("Designates the comment's likes"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Designates the comment creation date."),
    )

    def __str__(self):
        return self.content
