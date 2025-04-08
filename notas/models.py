
"""
class nota(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Create your models here.

"""

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField # type: ignore


class Nota(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = RichTextUploadingField()
    imagen = models.ImageField(upload_to='notas/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo