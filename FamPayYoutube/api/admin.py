from django.contrib import admin
from api.models import Video, ApiToken

admin.site.register([Video, ApiToken])
