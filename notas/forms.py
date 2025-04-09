from django import forms
from .models import Nota


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'descripcion', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'imagen': 'Imagen',
        }