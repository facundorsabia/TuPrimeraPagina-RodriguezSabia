from django.urls import path
from AppCoder import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    ### Login / Logout / Register
    path('registro', views.registro_view, name='registro'),
    path('login', views.login_view, name='login'),
    path('logout', LogoutView.as_view(template_name='AppCoder/logout.html'), name='logout'),

    path('Inicio/', views.inicio, name="Inicio"),
    path('MiMuro', views.muro, name="MiMuro"),
    path('CrearPublicacion', views.publicar, name="CrearPublicacion"),
    path('Hilo', views.hilo, name="Hilo"),
    path('buscar/', views.buscar_publicaciones, name="Busqueda"),
    path('cargar_formulario_comentario', views.cargar_formulario_comentario, name='cargar_formulario_comentario'),
    path('crear_comentario/', views.crear_comentario, name='crear_comentario'),

    #path('publicaciones/', views.PublicacionListView.as_view(), name='publicaciones'),
    #path('publicacion/<int:pk>', views.PublicacionDetailView.as_view(), name='publicacion-detail'),
    #path('publicacion/create/', views.PublicacionCreateView.as_view(), name='publicacion_create'),
    #path('publicacion/<int:pk>/update/', views.PublicacionUpdateView.as_view(), name='publicacion_update'),
    #path('publicacion/<int:pk>/delete/', views.PublicacionDeleteView.as_view(), name='publicacion_delete'),
]