from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='home'),
    path('notas/', views.notas_view, name='notas'),
    path('notas/create/', views.notas_create, name='create'),
    path('notas/edit/<int:nota_id>/', views.notas_edit, name='edit'),
    path('notas/delete/<int:nota_id>/', views.notas_delete, name='delete'),
    path('perfil/',views.perfil,name='perfil'),
    path('notas/detail/<int:nota_id>/',views.nota_detail,name='detail'),
    path("logout/", views.logout_view, name="logout"),
    path('login/', LoginView.as_view(template_name='notas/login.html'), name='login'),
    path('register/', views.create_user, name='register'),
    path('categorias/', views.categorias_list, name='categorias_list'),
    path('categorias/create/', views.categoria_create, name='categoria_create'),
    path('categorias/delete/<int:categoria_id>/', views.categoria_delete, name='categoria_delete'),
    path('borrar-imagen/', views.borrar_imagen, name='borrar_imagen'),

]