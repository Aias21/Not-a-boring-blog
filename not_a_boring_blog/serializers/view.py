from rest_framework import serializers


class ViewCountSerializer(serializers.Serializer):
    views_count = serializers.IntegerField()