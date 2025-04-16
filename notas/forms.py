from django import forms
from .models import Nota, Categoria, Profile
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
    
class UserCreationFormWithImage(UserCreationForm):
    profile_picture = forms.ImageField(required=False, label="Foto de perfil")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'profile_picture')
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile_picture = self.cleaned_data.get('profile_picture')
        # Crea el perfil incluso si no hay imagen
            Profile.objects.create(user=user, profile_picture=profile_picture if profile_picture else None)
        return user
    
