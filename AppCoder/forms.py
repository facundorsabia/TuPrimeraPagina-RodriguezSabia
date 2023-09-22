from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class UsuarioForm(forms.Form):
    usuario = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput)

class PublicacionForm(forms.Form):  
    contenido = forms.CharField(
        label="Contenido",
        max_length=280,
        widget=forms.Textarea(attrs={'class': 'form-control input-white', 'style': 'width: 100%;', 'rows': 3}),
    )

class ComentarioForm(forms.Form): 
    contenido = forms.CharField(
        label="Contenido",
        max_length=280,
        widget=forms.Textarea(attrs={'class': 'form-control input-white', 'style': 'width: 100%;', 'rows': 3}),
    )

#Formulario de Registro
class UserCreationFormulario(UserCreationForm):
    username = forms.CharField(label="Usuario")
    email = forms.EmailField(label="Correo Electrónico")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {k:"" for k in fields}

#Formulario de edición de usuario
class UserEditionFormulario(UserChangeForm):
    email = forms.EmailField()
    username = forms.CharField(label="Usuario")
    password = None

    class Meta:
        model = User
        fields = ["username", "email"]
        help_texts = {k: "" for k in fields}
        

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        

class PublicacionEditForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['contenido'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contenido'].widget.attrs.update({'class': 'form-control', 'rows': 3})