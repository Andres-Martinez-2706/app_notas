from django.shortcuts import render,redirect,get_object_or_404
from .forms import NotaForm
from .models import Nota
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    print(request.user)
    return render(request,'notas/base.html')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect("login")

@login_required
def notas_view(request):
    
    if request.user.is_superuser or request.user.is_staff:
        notas = Nota.objects.order_by('-created_at')  # Muestra solo los del usuario actual
    else:
        notas = Nota.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'notas/notas.html', {'notas': notas})

@login_required
def perfil(request):
    notas = Nota.objects.filter(author=request.user).order_by('-created_at')  # Muestra solo los del usuario actual
    return render(request, 'notas/perfil.html', {'notas': notas})

@login_required
def notas_edit(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    if request.method == 'POST':
        form = NotaForm(request.POST, request.FILES, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('notas')
    else:
        form = NotaForm(instance=nota)
    return render(request, 'notas/notas_edit.html', {'form': form})

@login_required
def notas_create(request):
    if request.method == 'POST':
        form = NotaForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # Asignar el usuario actual
            note.save()
            return redirect('notas')
    else:
        form = NotaForm()
    return render(request, 'notas/notas_create.html', {'form': form})


@login_required
def nota_detail(request, nota_id):
    note = get_object_or_404(Nota, id=nota_id)
    return render(request, 'notas/nota_detail.html', {
        'nota': note,

    })

@login_required
def notas_delete(request, nota_id):

    nota = get_object_or_404(Nota, id=nota_id)
    nota.delete()
    return redirect('notas')



# Create your views here.
