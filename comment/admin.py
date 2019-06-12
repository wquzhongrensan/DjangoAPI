from django.contrib import admin
from comment.models import Post, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_time', 'title', 'excerpt')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'pub_time', 'body', 'in_post', 'reply_comment')


# 注册三个model
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)