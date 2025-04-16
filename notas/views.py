from django.shortcuts import render,redirect,get_object_or_404
from .forms import NotaForm, UserCreationFormWithImage
from .models import Nota, Categoria
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q

def create_user(request):
    if request.method == 'POST':
        form = UserCreationFormWithImage(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notas')
        else:
            return render(request, 'notas/create_user.html', {
                'form': form,
            })
    else:
        form = UserCreationFormWithImage()
    return render(request, 'notas/create_user.html', {
        'form': form,
    })

    

def index(request):
    print(request.user)
    return render(request,'notas/index.html')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect("login")

@login_required
def notas_view(request):
    # Obtener el término de búsqueda
    query = request.GET.get('q', '').strip()  # Elimina espacios vacíos
    print("🔍 Buscando:", repr(query))  # Imprime con repr para depuración

    # Filtrar notas según el tipo de usuario
    if request.user.is_superuser or request.user.is_staff:
        notas = Nota.objects.all()  # Superusuarios y staff ven todas las notas
    else:
        notas = Nota.objects.filter(author=request.user)  # Usuarios normales ven solo sus notas

    # Aplicar el filtro de búsqueda si hay un término
    if query:
        notas = notas.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )

    # Ordenar las notas por fecha de creación (más reciente primero)
    notas = notas.order_by('-created_at')

    # Depuración: Mostrar las notas filtradas
    print("Notas filtradas:", list(notas.values('id', 'titulo', 'descripcion')))

    return render(request, 'notas/notas.html', {'notas': notas, 'query': query})

@login_required
def perfil(request):
    notas = Nota.objects.filter(author=request.user).order_by('-created_at')
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = ProfileImageForm(instance=profile)

    return render(request, 'notas/perfil.html', {
        'notas': notas,
        'form': form
    })


@login_required
def notas_edit(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id, author=request.user)
    if request.method == 'POST':
        form = NotaForm(request.user, request.POST, request.FILES, instance=nota)
        if form.is_valid():
            # Guardar la nota sin guardar las relaciones ManyToMany todavía
            nota = form.save(commit=False)
            nota.save()  # Guardar la nota en la base de datos
            form.save_m2m()  # Guardar las categorías seleccionadas en el formulario

            # Manejar nueva categoría
            nueva_categoria = form.cleaned_data.get('nueva_categoria')
            if nueva_categoria:
                categoria, created = Categoria.objects.get_or_create(nombre=nueva_categoria)
                categoria.usuarios.add(request.user)
                nota.categorias.add(categoria)  # Añadir la nueva categoría

            return redirect('notas')
    else:
        form = NotaForm(user=request.user, instance=nota)
    return render(request, 'notas/notas_edit.html', {'form': form, 'nota': nota})

@login_required
def notas_create(request):
    if request.method == 'POST':
        form = NotaForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            # Guardar la nota sin guardar las relaciones ManyToMany todavía
            nota = form.save(commit=False)
            nota.author = request.user  # Asignar el usuario actual
            nota.save()  # Guardar la nota en la base de datos
            form.save_m2m()  # Guarda las categorías seleccionadas en el formulario

            # Manejar nueva categoría
            nueva_categoria = form.cleaned_data.get('nueva_categoria')
            if nueva_categoria:
                # Asegurarse de que la categoría se cree y guarde correctamente
                categoria, created = Categoria.objects.get_or_create(nombre=nueva_categoria)
                categoria.usuarios.add(request.user)
                # Añadir la nueva categoría a la nota
                nota.categorias.add(categoria)

            return redirect('notas')
    else:
        form = NotaForm(user=request.user)
    return render(request, 'notas/notas_create.html', {'form': form})

@login_required
def nota_detail(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id,author=request.user)
    return render(request, 'notas/nota_detail.html', {
        'nota': nota,
    })

@login_required
def notas_delete(request, nota_id):

    nota = get_object_or_404(Nota, id=nota_id)
    nota.delete()
    return redirect('notas')


@login_required
def categorias_list(request):
    categorias = Categoria.objects.filter(Q(usuarios=request.user) | Q(es_predeterminada=True))
    return render(request, 'notas/categorias_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            categoria, created = Categoria.objects.get_or_create(nombre=nombre)
            categoria.usuarios.add(request.user)
            return redirect('categorias_list')
    return render(request, 'notas/categoria_form.html')

@login_required
def categoria_delete(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if not categoria.es_predeterminada and request.user in categoria.usuarios.all():
        categoria.usuarios.remove(request.user)
        if not categoria.usuarios.exists() and not categoria.notas.exists():
            categoria.delete()
    return redirect('categorias_list')

@login_required
def borrar_imagen(request):
    profile = request.user.profile
    if profile.profile_picture:
        profile.profile_picture.delete()
        profile.save()
    return redirect('perfil')