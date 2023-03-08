from django.db import models
import datetime
# Create your models here.

class BaseField(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=False, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True