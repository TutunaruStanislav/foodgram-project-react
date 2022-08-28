import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers

FILENAME_STR_OFFSET = 9


class Base64Field(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            img_format, imgstr = data.split(';base64,')
            ext = img_format.split('/')[-1]
            name = uuid.uuid4()
            data = ContentFile(
                base64.b64decode(imgstr),
                name=name.urn[FILENAME_STR_OFFSET:] + '.' + ext
            )

        return super().to_internal_value(data)
