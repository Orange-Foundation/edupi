import copy

from rest_framework import serializers

from .models import Directory, Document


class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ('id', 'url', 'name')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'description', 'file', 'thumbnail')

    def create(self, validated_data):
        if validated_data['thumbnail']:
            return super().create(validated_data)

        # generate thumbnail here
        uploaded_file = validated_data['file']
        content_type = uploaded_file.content_type

        if content_type in ['image/jpeg', 'image/png']:
            validated_data['thumbnail'] = copy.deepcopy(validated_data['file'])

        elif content_type in ['application/pdf']:
            print('pdf uploaded, todo')

        elif content_type in ['video/mp4']:
            print('mp4 uploaded, todo')

        elif content_type in ['audio/mpeg']:
            print('mp3 uploaded, todo')

        else:
            pass

        return super().create(validated_data)
