from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class LokiPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'status': 'success',
            'results': data,
            'meta': {
                'count': self.page.paginator.count,
                'page': self.page.number,
                'limit': self.get_page_size(self.request),
                'total_pages': self.page.paginator.num_pages
            }
        })
