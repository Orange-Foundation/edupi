from rest_framework import serializers

from .models import Directory


class DirectorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Directory
        fields = ('id', 'name', 'sub_dirs', 'documents')
