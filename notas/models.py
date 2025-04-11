from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField # type: ignore
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Nombre único para evitar duplicados
    es_predeterminada = models.BooleanField(default=False)  # Indica si es una categoría predeterminada
    usuarios = models.ManyToManyField(User, related_name='categorias', blank=True)  # Usuarios que usan esta categoría

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        # Al eliminar una categoría, se remueve de todas las notas asociadas
        notas = Nota.objects.filter(categorias=self)
        for nota in notas:
            nota.categorias.remove(self)
        super().delete(*args, **kwargs)

class Nota(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = RichTextUploadingField()
    imagen = models.ImageField(upload_to='notas/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    categorias = models.ManyToManyField(Categoria, blank=True, related_name='notas')  # Relación muchos a muchos con categorías
    
    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
    
    def __str__(self):
        return self.titulo