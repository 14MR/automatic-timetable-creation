from rest_framework import pagination
from rest_framework.response import Response


class LimitOffsetSimplePagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(data, headers={'X-total': self.count})
