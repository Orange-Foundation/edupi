import datetime

from rest_framework import status
from rest_framework.decorators import detail_route
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from django.core.cache import cache
from django.db import transaction
from django.utils.encoding import force_text
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor import bits

from cntapp.helpers import get_root_dirs
from cntapp.serializers import DirectorySerializer, DocumentSerializer
from cntapp.models import Directory, Document


class UpdatedAtKeyBit(bits.KeyBitBase):
    """
    Cache every read request and invalidate all cache data after write to any model,
    which used in API.
    This approach let us don't think about granular cache invalidation - just flush
    it after any model instance change/creation/deletion.
    """

    def get_data(self, **kwargs):
        key = 'api_updated_at_timestamp'
        value = cache.get(key, None)
        if not value:
            value = datetime.datetime.utcnow()
            cache.set(key, value=value)
        return force_text(value)


class CustomObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = bits.RetrieveSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()


class CustomListKeyConstructor(DefaultKeyConstructor):
    """ For calculating the key of the cache """
    all_query_params = bits.QueryParamsKeyBit('*')
    kwargs = bits.KwargsKeyBit('*')
    pagination = bits.PaginationKeyBit()
    list_sql = bits.ListSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()


def index(request):
    return render(request, 'cntapp/index.html')


class DocumentViewSet(viewsets.ModelViewSet):
    """
    This viewset list `documents`, and provides `create`, `retrieve`,
    `update` and `destroy` options
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @cache_response(key_func=CustomObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @cache_response(key_func=CustomListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DirectoryViewSet(viewsets.ModelViewSet):
    """
    This viewset list `directories`, and provides `create`, `retrieve`,
    `update` and `destroy` options

    We can also `create_sub_directory`, list `sub_directories`, in detailed objects.
    To access root directories, append `?root=true` on the url.
    Use `sub_content` to get both `sub_directories` and `documents`
    """
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer

    @cache_response(key_func=CustomObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @cache_response(key_func=CustomListKeyConstructor())
    def list(self, request, *args, **kwargs):
        # filter root directories here instead of using get_queryset
        # because we can't construct a this queryset!
        is_root = self.request.QUERY_PARAMS.get('root', None)
        if is_root is not None and is_root == 'true':
            serializer = DirectorySerializer(get_root_dirs(), many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return super(DirectoryViewSet, self).list(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def create_sub_directory(self, request, *args, **kwargs):
        serializer = DirectorySerializer(data=request.data)
        if serializer.is_valid():
            new_dir = serializer.save()
            self.get_object().add_sub_dir(new_dir)
            return Response({'status': 'sub directory created'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'])
    @cache_response(key_func=CustomListKeyConstructor())
    def sub_directories(self, request, *args, **kwargs):
        current_dir = self.get_object()
        serializer = DirectorySerializer(current_dir.get_sub_dirs(), many=True, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['get'])
    @cache_response(key_func=CustomListKeyConstructor())
    def sub_content(self, request, *args, **kwargs):
        current_dir = self.get_object()
        dirs = DirectorySerializer(current_dir.get_sub_dirs(), many=True, context={'request': request})
        docs = DocumentSerializer(current_dir.documents, many=True, context={'request': request})
        return Response({
            'directories': dirs.data,
            'documents': docs.data
        })

    @transaction.atomic
    def perform_destroy(self, instance):
        """ Delete recursively a directory
        """
        sub_dirs = instance.get_sub_dirs()
        for d in sub_dirs:
            instance.remove_sub_dir(d)
        super().perform_destroy(instance)

    @detail_route(methods=['delete'])
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        """ Delete recursively a sub directory
        """
        if 'id' not in request.data:
            return Response(data={'status': 'no sub-directory id is provided'},
                            status=status.HTTP_400_BAD_REQUEST)
        dir_id = int(request.data['id'])
        sub_dir = get_object_or_404(Directory, pk=dir_id)
        self.get_object().remove_sub_dir(sub_dir)
        return Response({'status': 'sub directory deleted'})

    @detail_route(methods=['get'])
    @cache_response(key_func=CustomListKeyConstructor())
    def paths(self, request, *args, **kwargs):
        """calculate all the paths to this directory"""
        all_paths = self.get_object().get_paths()
        data = []
        for path in all_paths:
            serializer = DirectorySerializer(path, many=True, context={'request': request})
            data.append(serializer.data)
        return Response(data)

    @detail_route(methods=['post', 'delete'])
    def directories(self, request, *args, **kwargs):
        if 'id' not in request.data:
            return Response(data={'status': 'no sub-directory id is provided'},
                            status=status.HTTP_400_BAD_REQUEST)
        dir_id = int(request.data['id'])
        sub_dir = get_object_or_404(Directory, pk=dir_id)
        current_dir = self.get_object()

        if request.method == 'POST':
            current_dir.add_sub_dir(sub_dir)
            return Response(data={'status': 'relation created'}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if current_dir.unlink_sub_dir(sub_dir):
                return Response({'status': 'sub directory unlinked'})
            else:
                return Response({'status': 'Relation does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @detail_route(methods=['post', 'get', 'delete'])
    def documents(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get_documents(request, *args, **kwargs)
        elif request.method == 'POST':
            return self.add_documents(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.delete_documents(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    def _check_json_documents_in_request(request):
        if not isinstance(request.data, dict):
            return Response({'status': 'JSON data is expected'}, status=status.HTTP_400_BAD_REQUEST)

        if 'documents' not in request.data:
            return Response({'documents': 'This field should contain a list of document id'},
                            status=status.HTTP_400_BAD_REQUEST)

    @cache_response(key_func=CustomListKeyConstructor())
    def get_documents(self, request, *args, **kwargs):
        current_dir = self.get_object()
        serializer = DocumentSerializer(current_dir.documents, many=True, context={'request': request})
        return Response(serializer.data)

    def add_documents(self, request, *args, **kwargs):
        res = self._check_json_documents_in_request(request)
        if res is not None:
            return res

        if isinstance(request.data['documents'], str):
            documents_id = [int(request.data['documents'])]
        else:
            documents_id = [int(d) for d in request.data['documents']]

        documents = Document.objects.filter(pk__in=documents_id)
        if documents.count() != len(documents_id):
            return Response({'status': 'document objects not exist!'}, status=status.HTTP_404_NOT_FOUND)

        self.get_object().documents.add(*documents)
        return Response(status=status.HTTP_201_CREATED)

    def delete_documents(self, request, *args, **kwargs):
        res = self._check_json_documents_in_request(request)
        if res is not None:
            return res

        if isinstance(request.data['documents'], str):
            documents_id = [int(request.data['documents'])]
        else:
            documents_id = [int(d) for d in request.data['documents']]

        current_dir = self.get_object()
        documents = current_dir.documents.filter(pk__in=documents_id)
        if documents.count() != len(documents_id):
            return Response({'status': 'documents not exist in directory!'}, status=status.HTTP_404_NOT_FOUND)

        current_dir.documents.remove(*documents)
        return Response(status=status.HTTP_200_OK)
