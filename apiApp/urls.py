from django.conf.urls import include
from django.urls import path
from  rest_framework import routers
from apiApp import views
from rest_framework.documentation import include_docs_urls


API_TITLE = 'API Documents'
API_DESCRITION = 'API Information'


route = routers.DefaultRouter()
route.register(r'test', views.TestViewSet)
route.register(r'snippet', views.SnippetView)
route.register(r'group', views.GroupView)

urlpatterns = [
    path('', include(route.urls)),

    path(r'docs/', include_docs_urls(title=API_TITLE, description=API_DESCRITION, authentication_classes=[], permission_classes=[]))
]