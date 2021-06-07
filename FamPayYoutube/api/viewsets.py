from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from api.models import Video, ApiToken
from api.serializers import VideoSerializer, ApiKeySerializer

class VideoViewset(viewsets.ModelViewSet):
    '''
    '''
    http_method_names = ['get']
    permission_classes =  (AllowAny,)
    queryset = Video.objects.all().order_by('-published_date')
    serializer_class = VideoSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter,  DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = search_fields

class ApiKeyViewset(viewsets.ModelViewSet):
    '''
    '''

    http_method_names = ['get','post']
    permission_classes = (AllowAny)
    queryset = ApiToken.objects.all()
    serializer_class = ApiKeySerializer
