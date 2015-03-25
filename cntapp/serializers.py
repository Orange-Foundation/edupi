from rest_framework import serializers

from .models import Directory


class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ('url', 'name')
