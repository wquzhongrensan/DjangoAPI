from django.shortcuts import render
from rest_framework import viewsets
from apiApp.models import TestModel, Snippet, Group
from apiApp.serializers import TestModelSerializer, SnippetSerializers, GroupSerializers
from rest_framework.versioning import URLPathVersioning

from apiApp.models import Question, Questionnaire, Choice
from django.http import JsonResponse
from django.views import View
import json


# Create your views here.
# 视图的种类
# GenericAPIView，RetrieveModelMixin，GenericViewSet

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
        return JsonResponse({'msg': 'success save'})


class QuestionnaireDetail(View):
    '''获取id为questionnaire_id的问卷'''

    def get(self, request, questionnaire_id):
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        data = questionnaire.questionnaire_to_dict()
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

