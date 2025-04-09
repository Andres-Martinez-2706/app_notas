from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField # type: ignore
from django.contrib.auth.models import User

class Nota(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = RichTextUploadingField()
    imagen = models.ImageField(upload_to='notas/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.titulo