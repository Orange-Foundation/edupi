from rest_framework import status
from rest_framework.decorators import detail_route
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets

from cntapp.helpers import get_root_dirs
from cntapp.serializers import DirectorySerializer
from cntapp.models import Directory


def index(request):
    return render(request, 'cntapp/index.html')


def root(request):
    return directory(request)


def directory(request, dir_id=None):
    if dir_id is None:
        dirs = [d for d in (Directory.objects.all()) if d.get_parents().count() == 0]
    else:
        d = get_object_or_404(Directory, pk=dir_id)
        dirs = d.get_sub_dirs()

    return render(request, 'cntapp/dir_list.html', {'dirs': dirs})


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
            return super(DirectoryViewSet, self).list(request,*args, **kwargs)

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

    @detail_route(methods=['put'])
    def update(self, request, *args, **kwargs):
        current_dir = self.get_object()
        serializer = DirectorySerializer(data=request.data)
        if serializer.is_valid():
            current_dir.name = serializer.validated_data.get('name')
            current_dir.save()
        return Response({'status': 'directory updated'})

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


