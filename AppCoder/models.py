from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Publicacion(models.Model):
    contenido = models.CharField(max_length=280)  # Limitamos el contenido a 280 caracteres (simulando la restricción de Twitter)
    autor_nombre = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Publicación de {self.autor_nombre}: {self.contenido[:50]}...'  # Mostrar una vista previa del contenido

class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    autor_nombre = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor_nombre} en la publicación de {self.publicacion.autor_nombre}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

