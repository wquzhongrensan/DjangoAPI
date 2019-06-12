from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as drf_views
from apiApp import views
from rest_framework.documentation import include_docs_urls
from apiApp.views import Questions, Questionnaires, QuestionDetail, QuestionnaireDetail

from apiApp.views import Questionnaire_Detail, QuestionnaireList, QuestionList

from rest_framework_jwt.views import obtain_jwt_token

API_TITLE = 'API Documents'
API_DESCRITION = 'API Information'


router = routers.DefaultRouter()
router.register(r'test', views.TestViewSet)
router.register(r'snippet', views.SnippetView)
router.register(r'group', views.GroupView)
router.register(r'regions', views.RegionViewSet, base_name='regions')
router.register(r'machine_rooms', views.MachineRoomViewSet, base_name='machine_rooms')
router.register(r'cabinets', views.CabinetViewSet, base_name='cabinets')
router.register(r'devices', views.DeviceViewSet, base_name='devices')
router.register(r'servers', views.ServerViewSet, base_name='servers')

urlpatterns = [
    path('', include(router.urls)),

    path(r'docs/', include_docs_urls(title=API_TITLE, description=API_DESCRITION, authentication_classes=[], permission_classes=[])),

    # path(r'testapi/<str:version>/detail/', xxxxx.as_view()),

    # 通过django 自身
    url(r'^questions/$', Questions.as_view(), name='questions'),
    url(r'^questionnaire/(?P<questionnaire_id>\d+)/$', QuestionnaireDetail.as_view(), name='questionnaire'),
    url(r'^questionnaires/$', Questionnaires.as_view(), name='questionnaires'),

    url(r'^question/(?P<question_id>\d+)/$', QuestionDetail.as_view(), name='question'),

    # 通过 django rest framework
    url(r'^questions/$',QuestionList.as_view(),name='questions'),
    url(r'^questionnaire/(?P<pk>\d+)/$',Questionnaire_Detail.as_view(),name='questionnaire'),
    url(r'^questionnaires/$',QuestionnaireList.as_view(),name='questionnaires'),

    # 全局搜索入口
    url(r'^search/', include('haystack.urls')),

    # 根据用户名和密码 换取 身份验证令牌
    url(r'^auth/', drf_views.obtain_auth_token, name='auth'),
    url(r'^api-token-auth/', obtain_jwt_token),
]