from django.urls import path

from AppCoder import views


urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('MiMuro', views.muro, name="MiMuro"),
    path('CrearPublicacion', views.publicar, name="CrearPublicacion"),
    path('Hilo', views.hilo, name="Hilo"),
    path('buscar/', views.buscar_publicaciones, name="Busqueda"),
    path('cargar_formulario_comentario', views.cargar_formulario_comentario, name='cargar_formulario_comentario'),
    path('crear_comentario/', views.crear_comentario, name='crear_comentario'),
]