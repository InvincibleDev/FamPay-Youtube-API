from rest_framework import serializers
from api.models import Video, ApiToken

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = (
            "video_id",
            "title",
            "description",
            "thumbnail_url",
            "published_date",
            )

class ApiKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiToken
        fields = (
            'token',
            'is_exhausted',
        )
