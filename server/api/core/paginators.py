from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class BasePageNumberPaginator(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ("count", self.page.paginator.count),
            ("num_pages", self.page.paginator.num_pages),
            ("current", self.page.number),
            ("next", self.get_next_link()),
            ("previous", self.get_previous_link()),
            ("results", data)
        ]))
