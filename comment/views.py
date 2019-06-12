from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from .serializer import *

# 评论相关视图处理
class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    处理 /api/comments POST, 处理 /api/comments/<pk> GET
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """
        重写 perform_create
        user 信息不在 request.data 中, 在保存时加入 user 信息
        """
        serializer.save(user=self.request.user)

