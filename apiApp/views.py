from django.shortcuts import render
from rest_framework import viewsets
from apiApp.models import TestModel, Snippet, Group
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response

from .permissions import *
from .serializers import *
from .filters import *
from .paginations import *

from django_filters import rest_framework
from rest_framework import filters

from apiApp.models import Question, Questionnaire, Choice, Server
from django.http import JsonResponse
from django.views import View
import json


# Create your views here.
# 视图的种类
# GenericAPIView，RetrieveModelMixin，GenericViewSet

class TestViewSet(viewsets.ModelViewSet):
    queryset = TestModel.objects.all().order_by('-pk')  # 指定结果集
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


# class OrderDetailView(APIView):
#     versioning_class = URLPathVersioning
#
#     def get(self, request, version):
#         data = {}
#         version = request.version
#         if version == 'v1':
#             data['result'] = ORDER_DETAIL
#         elif version == 'v2':
#             data['results'] = {
#                 'goods': [
#                     {'name': '苹果'},
#                     {
#                         'name': '香蕉'
#                     }
#                 ]
#             }
#         return JsonResponse(data)

class Questionnaires(View):
    def get(self, request):
        # 获取所有问卷
        data = []
        questionnaires = Questionnaire.objects.all()  # 获取所有的问卷类
        for questionnaire in questionnaires:
            data.append(questionnaire.questionnaire_to_dict())
        return JsonResponse({'data': data})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        questionnaire = Questionnaire(title=data.get('title'))
        questionnaire.save()
        #  提交只返回结果 不返回对应实体
        return JsonResponse({'msg': 'success save'})


class QuestionnaireDetail(View):
    '''获取id为questionnaire_id的问卷'''

    def get(self, request, questionnaire_id):
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        data = questionnaire.questionnaire_to_dict()
        # 返回json
        return JsonResponse(data)

# 获取所有问题对象数据，及添加问题对象
class Questions(View):

    def get(self,request):
        #查询所有问题
        questions_set = Question.objects.all()
        #把question_set转化为字典
        data = []
        for question in questions_set:
            data.append(question.question_to_dict())
        #把字典数据当做json返回
        return JsonResponse({'data':data})

    def post(self,request,*args,**kwargs):
        '''假设前端通过post传过来一个json数据'''
        #把request中的json转化为python对象
        data = json.loads(request.body.decode())
        #抽取数据
        questionnaire_id = data.get('questionnaire_id')
        title = data.get('title')
        is_checkbox = data.get('is_checkbox')
        # 获取questionnaire_id对应的对象
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        #创建Question实例
        question = Question(title=title,is_checkbox=is_checkbox,questionnaire=questionnaire)
        question.save()
        #创建choice对象
        choices = data.get('choice')
        for c in choices:
            choice = Choice()
            choice.content = c
            choice.question = question
            choice.save()
        return JsonResponse({"msg":"success save"})


# 通过get,put,delete处理单个问题对象
class QuestionDetail(View):
    def delete(self, request, question_id):
        question = Question.objects.get(id=question_id)
        question.delete()

    def put(self, request, question_id):
        # 获取前端put的数据
        data = json.loads(request.body.decode())
        title = data.get('title')
        # 获取question对象
        question = Question.objects.get(id=question_id)
        question.title = title
        question.save()
        return JsonResponse({'msg': 'modify success'})

    def get(self, request, question_id):
        question = Question.objects.get(id=question_id)
        data = question.question_to_dict()
        return JsonResponse(data)


class QuestionnaireList(APIView):
    def get(self, request):
        questionnaire = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(questionnaire, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class Questionnaire_Detail(APIView):
    def get_object(self, pk):
        try:
            return Questionnaire.objects.get(pk=pk)
        except Questionnaire.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        questionnaire = self.get_object(pk)
        serializer = QuestionnaireSerializer(questionnaire)
        return Response(serializer.data)

    def put(self, request, pk):
        questionnaire = self.get_object(pk)
        serializer = QuestionSerializer(questionnaire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        questionnaire = self.get_object(pk)
        questionnaire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionList(APIView):
    def get(self, request):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# URL 对应的入口点
class RegionViewSet(viewsets.ModelViewSet):
    """
    区域操作视图
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    pagination_class = MyFormatResultsSetPagination
    permission_classes = (CustomerAccessPermission, )


class MachineRoomViewSet(viewsets.ModelViewSet):
    """
    机房操作视图
    """
    queryset = MachineRoom.objects.all()
    serializer_class = MachineRoomSerializer
    pagination_class = StandardResultsSetPagination


class CabinetViewSet(viewsets.ModelViewSet):
    """
    机柜操作视图
    """
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    pagination_class = LargeResultsSetPagination


class DeviceViewSet(viewsets.ModelViewSet):
    """
    设备操作视图
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = LargeResultsSetPagination


class ServerViewSet(viewsets.ModelViewSet):
    """
    物理服务器视图
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    pagination_class = MyFormatResultsSetPagination
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, )
    filter_class = ServerFilter
    search_fields = ('^server_name', '=brand', 'status', )
    ordering_fields = ('cpus', 'ram', 'disk', 'product_date', )
    ordering = ('-created_time', )
