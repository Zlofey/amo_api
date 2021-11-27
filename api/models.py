from django.db import models

# Create your models here.

class Token(models.Model):
    access = models.TextField()
    refresh = models.TextField()
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    expires_in = models.IntegerField()