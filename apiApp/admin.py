from django.contrib import admin
from apiApp.models import TestModel, Snippet, Group

# Register your models here.

# 如果这里不注册 后台管理不会显示
@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'age')   # 在后台管理系统中需要显示的字段

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('created', 'title', 'code', 'linenos', 'group')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('class_room', 'number')