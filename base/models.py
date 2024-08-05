import os
from contextlib import suppress

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete


# Create your models here.
class Suggestions(models.Model):
    name = models.CharField(max_length=64)
    phone = models.BigIntegerField()
    email = models.EmailField()
    content = models.TextField(max_length=1024)

    def __str__(self) -> str:
        return self.content[:200]


class FileData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="upload")

    def delete_handler(instance, **kwargs):
        with suppress(Exception):
            os.remove(instance.file.path)


post_delete.connect(FileData.delete_handler, sender=FileData)
