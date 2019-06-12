from rest_framework import pagination
from  rest_framework.response import Response


class LargeResultsSetPagination(pagination.PageNumberPagination):
    """
    大型分页方法
    """
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(pagination.PageNumberPagination):
    """
    标准分页方法
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class MyFormatResultsSetPagination(pagination.PageNumberPagination):

    page_size_query_param = "page_size"
    page_query_param = 'page'
    page_size = 10
    max_page_size = 1000

    """
    自定义分页方法
    """
    def get_paginated_response(self, data):
        """
        设置返回内容格式
        """
        return Response({
            'results': data,
            'pagination': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'page': self.page.start_index() // self.page.paginator.per_page + 1})