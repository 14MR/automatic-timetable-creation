from rest_framework import pagination
from rest_framework.response import Response


class TimurSmartPagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(data)
