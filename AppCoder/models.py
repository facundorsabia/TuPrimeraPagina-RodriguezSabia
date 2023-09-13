from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class CrearUsuario(models.Model):
    usuario = models.CharField(max_length=255)
    contraseña = models.CharField(max_length=255)  # En una aplicación real, deberías considerar el uso de un campo de contraseña más seguro como 'PasswordField'.

    def __str__(self):
        return self.usuario

class Publicacion(models.Model):
    contenido = models.CharField(max_length=280)  # Limitamos el contenido a 280 caracteres (simulando la restricción de Twitter)
    autor_nombre = models.CharField(max_length=50) 
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Publicación de {self.autor_nombre}: {self.contenido[:50]}...'  # Mostrar una vista previa del contenido

class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    autor_nombre = models.CharField(max_length=50)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor_nombre} en la publicación de {self.publicacion.autor_nombre}"