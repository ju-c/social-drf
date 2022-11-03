import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

# gettext_lazy will translate the string to the activated
# language if we defined a translation.
# See: https://docs.djangoproject.com/en/4.1/topics/i18n/translation/
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Email and password are required. Other fields are optional.
    """

    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    first_name = models.CharField(
        _("first name"),
        max_length=50,
        null=True,
        blank=True,
        help_text=_("Designates the user's first name."),
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        null=True,
        blank=True,
        help_text=_("Designates the user's last name."),
    )
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        help_text=_("Designates the user's username."),
    )
    biography = models.TextField(
        _("biography"),
        max_length=400,
        null=True,
        blank=True,
        default="",
        help_text=_("Designates the user's biography."),
    )
    current_activity = models.TextField(
        _("current activity"),
        max_length=400,
        null=True,
        blank=True,
        default="",
        help_text=_("Designates the user's current job or activity."),
    )
    location = models.CharField(
        _("location"),
        max_length=200,
        null=True,
        blank=True,
        default="",
        help_text=_("Designates the user's current location."),
    )
    date_of_birth = models.DateField(
        _("date of birth"),
        null=True,
        blank=True,
        help_text=_("Designates the user's date of birth."),
    )
    avatar = models.FileField(
        _("profile picture"),
        blank=True,
        null=True,
        upload_to="user/avatar/",
        help_text=_("Designates the user's avatar."),
    )
    cover_picture = models.FileField(
        _("cover picture"),
        blank=True,
        null=True,
        upload_to="user/cover_picture/",
        help_text=_("Designates the user's cover picture."),
    )
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    verified_account = models.BooleanField(
        _("verified account"),
        default=False,
        help_text=_(
            "Designates whether the account is real, credible, authentic and of interest to the public."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    private_account = models.BooleanField(
        _("private account"),
        default=False,
        help_text=_(
            "Designates whether this user account should be treated as private. "
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    following = models.ManyToManyField(
        "self", related_name="followers", blank=True, symmetrical=False
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username + "-" + self.email
