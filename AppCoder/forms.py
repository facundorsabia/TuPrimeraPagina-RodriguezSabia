from django import forms


class UsuarioForm(forms.Form):
    usuario = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput)

class PublicacionForm(forms.Form):
    autor_nombre = forms.CharField(
        label="Nombre del Autor",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control input-white', 'style': 'width: 100%;'})
    )    
    contenido = forms.CharField(
        label="Contenido",
        max_length=280,
        widget=forms.Textarea(attrs={'class': 'form-control input-white', 'style': 'width: 100%;', 'rows': 3}),
    )
    
class ComentarioForm(forms.Form):
    autor_nombre = forms.CharField(
        label="Nombre del Autor",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control input-white', 'style': 'width: 100%;'})
    )    
    contenido = forms.CharField(
        label="Contenido",
        max_length=280,
        widget=forms.Textarea(attrs={'class': 'form-control input-white', 'style': 'width: 100%;', 'rows': 3}),
    )