from django.shortcuts import render
from rest_framework import viewsets
from apiApp.models import TestModel, Snippet, Group
from apiApp.serializers import TestModelSerializer, SnippetSerializers, GroupSerializers

# Create your views here.

class TestViewSet(viewsets.ModelViewSet):
    queryset = TestModel.objects.all().order_by('-pk')  #  指定结果集
    serializer_class = TestModelSerializer


class SnippetView(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializers
    # filter_class = SnippetFilter
    search_fields = ('title', '=style',)


# viewset的写法是最简便的
class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializers


# 非viewset 视图
# class UserInfoPage(generics.ListAPIView):
#     queryset = UserInfo.objects.all()
#     serializer_class = UserInfoSerializer
#
#     # 单独写 对应的方法
#     def get(self, request, *args, **kwargs):
#         pageObject = UserInfo.objects.all()
#         page = self.paginate_queryset(pageObject)
#         _total = self._paginator.count
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             _list = serializer.data
#             return_dict = {
#                 'total': _total,
#                 'limit': 10,
#                 'list': _list
#             }
#             return Response(return_dict, status=status.HTTP_200_OK)
