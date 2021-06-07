from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.viewsets import VideoViewset, ApiKeyViewset
router=SimpleRouter()
router.register("youtubevideo", VideoViewset, basename="Youtube_Videos")
router.register("apikeys", ApiKeyViewset, basename="API Keys")

urlpatterns = [
    path('', include(router.urls) ),
]
