from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .serializers import UrineStripImageSerializer

class UrineStripImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = UrineStripImageSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            image_file_path = default_storage.save(image_file.name, ContentFile(image_file.read()))

            # here goes the processing

            # temp
            print(image_file_path)

            return Response(data={'path': image_file_path})
        return Response(serializer.errors, status=400)