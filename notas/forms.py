from django import forms
from .models import Nota, Categoria
from django.db.models import Q


class NotaForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),  # Mostrará todas las categorías disponibles
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    nueva_categoria = forms.CharField(max_length=100, required=False, label="Nueva categoría")
    
    class Meta:
        model = Nota
        fields = ['titulo', 'descripcion', 'imagen', 'categorias']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'imagen': 'Imagen',
        }
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar categorías: predeterminadas o usadas por el usuario
        self.fields['categorias'].queryset = Categoria.objects.filter(
            Q(usuarios=user) | Q(es_predeterminada=True)
        )