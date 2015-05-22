from rest_framework import status
from rest_framework.decorators import detail_route
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets

from cntapp.helpers import get_root_dirs
from cntapp.serializers import DirectorySerializer, DocumentSerializer
from cntapp.models import Directory, Document
from django.core import serializers


def index(request):
    return render(request, 'cntapp/index.html')


class DocumentViewSet(viewsets.ModelViewSet):
    """
    This viewset list `documents`, and provides `create`, `retrieve`,
    `update` and `destroy` options
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DirectoryViewSet(viewsets.ModelViewSet):
    """
    This viewset list `directories`, and provides `create`, `retrieve`,
    `update` and `destroy` options

    We can also `create_sub_directory`, list `sub_directories`, in detailed objects.
    To access root directories, append `?root=true` on the url.
    """
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer

    def perform_destroy(self, instance):
        sub_dirs = instance.get_sub_dirs()
        for d in sub_dirs:
            instance.remove_sub_dir(d)
        super().perform_destroy(instance)

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
    def sub_directories(self, request, *args, **kwargs):
        current_dir = self.get_object()
        serializer = DirectorySerializer(current_dir.get_sub_dirs(), many=True, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['delete'])
    def delete(self, request, *args, **kwargs):
        current_dir = self.get_object()
        serializer = DirectorySerializer(data=request.data)
        if serializer.is_valid():
            sub_dir = current_dir.get_sub_dir_by_name(serializer.validated_data.get('name'))

            current_dir.remove_sub_dir(sub_dir)
            return Response({'status': 'sub directory deleted'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        documents = Document.objects.filter(pk__in=documents_id)
        if documents.count() != len(documents_id):
            return Response({'status': 'document objects not exist!'}, status=status.HTTP_404_NOT_FOUND)

        self.get_object().documents.remove(*documents)
        return Response(status=status.HTTP_200_OK)
