from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def get_previous_next_pages(self):
    if self.page.has_next():
        next_page = self.page.number + 1
    else:
        next_page = None

    if self.page.has_previous():
        previous_page = self.page.number - 1
    else:
        previous_page = None
    return previous_page, next_page


class DefaultPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):
        previous_page, next_page = get_previous_next_pages(self)

        return Response(OrderedDict([
            ('page', self.page.number),
            ('count', self.page.paginator.count),
            ('next', next_page),
            ('previous', previous_page),
            ('results', data)
        ]))
