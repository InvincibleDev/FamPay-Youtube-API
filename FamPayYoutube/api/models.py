from django.db import models
from encrypted_fields import fields

class Video(models.Model):
    video_id = models.CharField(max_length = 100, unique=True)
    title = models.CharField(max_length = 100)
    description = models.TextField(null = True, blank = True)
    published_date = models.DateTimeField()
    thumbnail_url = models.URLField(null = True, blank = True)

    class Meta:
        app_label = 'api'
        db_table = 'VIDEO'

    def __str__(self):
        return self.title

class ApiToken(models.Model):
    token =  fields.EncryptedCharField(max_length=100)
    is_exhausted = models.BooleanField(default = False)

    class Meta:
        app_label = "api"
        db_table = "APITOKEN"

    def __str__(self):
        return self.token
