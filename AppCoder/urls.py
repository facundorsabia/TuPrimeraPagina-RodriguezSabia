from django.urls import path
from AppCoder import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    ### Login / Logout / Registro / Editar Usuario
    path('registro', views.registro_view, name='registro'),
    path('login', views.login_view, name='login'),
    path('logout', LogoutView.as_view(template_name='AppCoder/logout.html'), name='logout'),
    path('editar-usuario', views.editar_usuario_view, name="editar-usuario"),
    path('cambiar_contrasenia', views.CambiarContrasenia.as_view(), name='cambiar_contrasenia'),
    path('edicion_exitosa', views.edicion_exitosa, name='edicion_exitosa'), 
    
    ###Funciones de la App
    path('Inicio/', views.inicio, name="Inicio"),
    path('MiMuro', views.muro, name="MiMuro"),
    path('CrearPublicacion', views.publicar, name="CrearPublicacion"),
    path('eliminar-publicacion/<int:pk>/', views.PublicacionDelete.as_view(), name='eliminar_publicacion'),
    path('editar-publicacion/<int:pk>/', views.PublicacionUpdateView.as_view(), name='editar_publicacion'),
    path('buscar/', views.buscar_publicaciones, name="Busqueda"),
    path('cargar_formulario_comentario', views.cargar_formulario_comentario, name='cargar_formulario_comentario'),
    path('crear_comentario/', views.crear_comentario, name='crear_comentario'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)