from rest_framework import serializers

class UrineStripImageSerializer(serializers.Serializer):
    image = serializers.ImageField()