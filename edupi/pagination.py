from rest_framework.pagination import LimitOffsetPagination, CursorPagination
from rest_framework.response import Response
from rest_framework.compat import OrderedDict
from django.db.models import Q, CharField
import logging

logger = logging.getLogger(__name__)


class SimpleLimitOffsetPagination(LimitOffsetPagination):
    sort_query_param = 'sort'
    order_query_param = 'order'
    search_query_param = 'search'

    def paginate_queryset(self, queryset, request, view=None):
        search_term = request.query_params.get(self.search_query_param, None)
        if search_term is not None:
            fields = [f for f in queryset.model._meta.fields if isinstance(f, CharField)]
            queries = [Q(**{f.name + '__contains': search_term}) for f in fields]
            qs = Q()
            for query in queries:
                qs = qs | query
            queryset = queryset.filter(qs)

        sort_attr = request.query_params.get(self.sort_query_param, None)
        if sort_attr is not None:
            order = request.query_params.get(self.order_query_param, None)
            if order == 'desc':
                queryset = queryset.order_by('-' + sort_attr)
            elif order == 'asc':
                queryset = queryset.order_by(sort_attr)
            else:
                logger.warn('unexpected order param:' + order)

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.count),
            ('rows', data)
        ]))
