from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

min_bound, max_bound = settings.SHORT_URL_LENGTH_BOUNDS

class Urls(models.Model):
    short_id = models.CharField(max_length=max_bound, primary_key=True, unique=True)
    user_url = models.URLField(max_length=200)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts')

    def __str__(self):
        return self.user_url
