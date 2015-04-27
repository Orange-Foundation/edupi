import os
import tempfile
import copy

from django.core.files.uploadedfile import SimpleUploadedFile
from wand.image import Image
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
        if 'thumbnail' in validated_data:
            return super().create(validated_data)

        # generate thumbnail here
        uploaded_file = validated_data['file']
        content_type = uploaded_file.content_type

        if content_type in ['image/jpeg', 'image/png']:
            validated_data['thumbnail'] = copy.deepcopy(validated_data['file'])

        elif content_type in ['application/pdf']:
            file_name = None
            # use page[0] as thumbnail
            with Image(filename=validated_data['file'].temporary_file_path() + '[0]') as img:
                file_name = tempfile.mktemp(suffix='.png')
                img.save(filename=file_name)
            if file_name is not None:
                file_path = os.path.join('/tmp', file_name)
                with open(file_name, 'rb') as f:
                    validated_data['thumbnail'] = SimpleUploadedFile(file_name, f.read())

        elif content_type in ['video/mp4']:
            print('mp4 uploaded, todo')

        elif content_type in ['audio/mpeg']:
            print('mp3 uploaded, todo')

        else:
            pass

        return super().create(validated_data)
