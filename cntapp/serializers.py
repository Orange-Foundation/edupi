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
        fields = ('id', 'name', 'description', 'type', 'file', 'thumbnail')

    @staticmethod
    def fill_document_type(validated_data):
        content_type = validated_data['file'].content_type

        if content_type.startswith('image/'):
            validated_data['type'] = Document.TYPE_IMAGE
        elif content_type == 'application/pdf':
            validated_data['type'] = Document.TYPE_PDF
        elif content_type.startswith('video/'):
            validated_data['type'] = Document.TYPE_VIDEO
        elif content_type.startswith('audio/'):
            validated_data['type'] = Document.TYPE_AUDIO
        elif content_type == 'application/vnd.android.package-archive':
            validated_data['type'] = Document.TYPE_GOOGLE_APK
        else:
            validated_data['type'] = Document.TYPE_OTHERS

    def create(self, validated_data):
        self.fill_document_type(validated_data)
        if 'thumbnail' in validated_data:
            return super().create(validated_data)

        # generate thumbnail here
        uploaded_file = validated_data['file']
        content_type = uploaded_file.content_type

        if content_type in ['image/jpeg', 'image/png']:
            # copy the image for thumbnail
            with open(uploaded_file.temporary_file_path(), 'rb') as f:
                validated_data['thumbnail'] = SimpleUploadedFile(uploaded_file.name, f.read())

        elif content_type in ['application/pdf']:
            file_name = None
            # use page[0] as thumbnail
            with Image(filename=validated_data['file'].temporary_file_path() + '[0]') as img:
                file_name = tempfile.mktemp(suffix='.png')
                img.save(filename=file_name)  # save to /tmp
            if file_name is not None:
                file_path = os.path.join('/tmp', file_name)
                with open(file_name, 'rb') as f:
                    validated_data['thumbnail'] = SimpleUploadedFile(file_name, f.read())

        return super().create(validated_data)
