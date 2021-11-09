from django.db import models

RESOURCE_TYPES = ["image", "audio", "video", "puzzle"]


class Trait(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)


class Resource(models.Model):
    type = models.CharField(max_length=500, choices=RESOURCE_TYPES, blank=True, null=True)
    source = models.FilePathField(max_length=5000, blank=True, null=True)
