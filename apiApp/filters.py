import django_filters
from .models import *

# 过滤器使用的不是Django_rest_framework  而是 django_filters
class ServerFilter(django_filters.rest_framework.FilterSet):
    """
    物理服务器过滤器
    """

    server_name = django_filters.CharFilter(name='server_name', lookup_expr='icontains')
    brand = django_filters.CharFilter(name='brand', lookup_expr='icontains')
    cpus = django_filters.NumberFilter(name='cpus')
    ram = django_filters.NumberFilter(name='ram')
    disk = django_filters.NumberFilter(name='disk')

    class Meta:
        model = Server
        # 是代表可以根据这些字段来作为搜索字段吗
        fields = ['server_name', 'brand', 'cpus', 'ram', 'disk', ]