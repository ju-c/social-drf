from django.contrib import admin
from user_content.models import Post, Comment


# TabularInlin doc:
# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.TabularInline
class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    list_display = ("user", "truncated_content", "created_at")
    # ModelAdmin.exclude:
    # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.exclude
    exclude = ["comment", "parent_content"]

    # Limit the length of the text displayed in the
    # admin list display to 55 characters:
    def truncated_content(self, obj):
        return obj.content[:55]


admin.site.register(Post, PostAdmin)
