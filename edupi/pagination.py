from rest_framework.pagination import LimitOffsetPagination, CursorPagination
from rest_framework.response import Response
from rest_framework.compat import OrderedDict


class SimpleLimitOffsetPagination(LimitOffsetPagination):
    sort_query_param = 'sort'
    order_query_param = 'order'

    def paginate_queryset(self, queryset, request, view=None):
        sort_attr = request.query_params.get(self.sort_query_param, None)
        if sort_attr is not None:
            order = request.query_params.get(self.order_query_param, None)
            if order == 'desc':
                queryset = queryset.order_by('-' + sort_attr)
            elif order == 'asc':
                queryset = queryset.order_by(sort_attr)
            else:
                # todo warning
                pass

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.count),
            ('rows', data)
        ]))
