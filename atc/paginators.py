from rest_framework import pagination
from rest_framework.response import Response


class LimitOffsetSimplePagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        response = Response(data)
        response['X-total'] = len(data)
        return response
