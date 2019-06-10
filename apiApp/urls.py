from django.conf.urls import include, url
from django.urls import path
from  rest_framework import routers
from apiApp import views
from rest_framework.documentation import include_docs_urls
from apiApp.views import Questions, Questionnaires, QuestionDetail, QuestionnaireDetail

from apiApp.views import Questionnaire_Detail, QuestionnaireList, QuestionList

API_TITLE = 'API Documents'
API_DESCRITION = 'API Information'


route = routers.DefaultRouter()
route.register(r'test', views.TestViewSet)
route.register(r'snippet', views.SnippetView)
route.register(r'group', views.GroupView)

urlpatterns = [
    path('', include(route.urls)),

    path(r'docs/', include_docs_urls(title=API_TITLE, description=API_DESCRITION, authentication_classes=[], permission_classes=[])),

    # path(r'testapi/<str:version>/detail/', xxxxx.as_view()),

    url(r'^questions/$', Questions.as_view(), name='questions'),
    url(r'^questionnaire/(?P<questionnaire_id>\d+)/$', QuestionnaireDetail.as_view(), name='questionnaire'),
    url(r'^questionnaires/$', Questionnaires.as_view(), name='questionnaires'),

    url(r'^question/(?P<question_id>\d+)/$', QuestionDetail.as_view(), name='question'),


    url(r'^questions/$',QuestionList.as_view(),name='questions'),
    url(r'^questionnaire/(?P<pk>\d+)/$',Questionnaire_Detail.as_view(),name='questionnaire'),
    url(r'^questionnaires/$',QuestionnaireList.as_view(),name='questionnaires'),


]