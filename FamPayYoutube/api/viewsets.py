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
    Viewset for Video Model, can perform search on title and description using django-filters.
    Pagination done using PageNumberPagination.
    '''
    http_method_names = ['get']
    queryset = Video.objects.all().order_by('-published_date') # queryset ordered in reverse order of published data
    serializer_class = VideoSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter,  DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = search_fields

class ApiKeyViewset(viewsets.ModelViewSet):
    '''
    Viewset to add new API keys for youtube API.
    '''
    http_method_names = ['get','post']
    queryset = ApiToken.objects.all()
    serializer_class = ApiKeySerializer
