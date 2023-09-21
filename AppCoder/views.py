from django.shortcuts import render, redirect
from django.http import JsonResponse
from AppCoder.models import CrearUsuario, Publicacion, Comentario
from AppCoder.forms import UsuarioForm, PublicacionForm, ComentarioForm, UserCreationFormulario, UserEditionFormulario
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.auth.forms import PasswordChangeForm


def inicio(request):
      publicaciones = Publicacion.objects.all()
      return render(request, "AppCoder/inicio.html", {"publicaciones": publicaciones})


def muro(request):
      publicaciones = Publicacion.objects.all()
      return render(request, "AppCoder/mimuro.html", {"publicaciones": publicaciones})


def publicar(request):
      if request.method == 'POST':
            formulario = PublicacionForm(request.POST)
            if formulario.is_valid():
                  contenido = formulario.cleaned_data['contenido']
                  autor_nombre = request.user
                  publicacion = Publicacion(contenido=contenido, autor_nombre=autor_nombre)
                  publicacion.save()
                  publicaciones = Publicacion.objects.all()
                  return render(request, "AppCoder/mimuro.html", {"publicaciones": publicaciones}) #Vuelvo al mi muro
      else: 
            formulario= PublicacionForm() #Formulario vacio para construir el html
      return render(request, "AppCoder/publicar.html", {"formulario":formulario})


def buscar_publicaciones(request):
      if 'q' in request.GET:
            query = request.GET['q']
            # Busca las publicaciones que contienen la palabra clave en su contenido
            publicaciones = Publicacion.objects.filter(contenido__icontains=query)
      else:
            publicaciones = []
      return render(request, 'AppCoder/busqueda.html', {'publicaciones': publicaciones})


def crear_comentario(request):
      if request.method == 'POST':
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                  # Obtén los datos del formulario y crea el comentario
                  autor_nombre = request.user
                  contenido = comentario_form.cleaned_data['contenido']
                  publicacion_id = request.POST.get('publicacion_id')
                  publicacion = Publicacion.objects.get(id=publicacion_id)
                  comentario = Comentario(autor_nombre=autor_nombre, contenido=contenido, publicacion=publicacion)
                  comentario.save()

                  # Crea una representación HTML del comentario
                  comentario_html = f"""
                  <li class="list-group-item">
                        <h4>{comentario.autor_nombre}</h4>
                        <p>{comentario.contenido}</p>
                        <p>Fecha de publicación: {comentario.fecha_comentario}</p>
                  </li>
                  """

                  # Devuelve la representación HTML como respuesta JSON
                  return redirect('Inicio')

      # Maneja el caso en que no sea una solicitud POST o el formulario no sea válido
      return JsonResponse({'error': 'Error al crear el comentario'})


def cargar_formulario_comentario(request):
      publicacion_id = request.GET.get('publicacion_id')
      publicacion = Publicacion.objects.get(id=publicacion_id)

      # Renderiza el formulario de comentario y lo devuelve como una respuesta AJAX
      comentario_form = ComentarioForm()
      return render(request, 'AppCoder/formulario_comentario.html', {'comentario_form': comentario_form, 'publicacion': publicacion})

class PublicacionListView(ListView):
      model = Publicacion
      context_object_name = "publicaciones"
      template_name = "AppCoder/publicaciones_lista.html"

class PublicacionDetailView(DetailView):
      model = Publicacion
      context_object_name = "publicacionDetalle"
      template_name = "AppCoder/publicacion_detalle.html"

class PublicacionCreateView(CreateView):
      model = Publicacion
      template_name = "AppCoder/publicacion_crear.html"
      fields = ['autor_nombre','titulo', 'contenido']
      success_url = reverse_lazy('MiMuro')

class PublicacionUpdateView(UpdateView):
      model = Publicacion
      template_name = "AppCoder/publicacion_actualizar.html"
      fields = ['autor_nombre','titulo', 'contenido']

class PublicacionDeleteView(DeleteView):
      model = Publicacion
      template_name = "AppCoder/publicacion_eliminar.html"
      success_url = reverse_lazy('MiMuro')

#Login, Logout, Registro y Editar Usuario

def registro_view(request):

      if request.method == "GET":
            return render(
            request,
            "AppCoder/registro.html",
            {"form": UserCreationFormulario()}
            )
      else:
            formulario = UserCreationFormulario(request.POST)
            if formulario.is_valid():
                  informacion = formulario.cleaned_data
                  usuario = informacion["username"]
                  password = informacion["password1"]
                  formulario.save()

                  user = authenticate(request, username=usuario, password=password)
                  if user is not None:
                        login(request, user)
                        return render(
                              request,
                              "AppCoder/registro.html",
                              {"mensaje": f"Usuario creado: {usuario}"}
                        )
            else:
                  return render(
                        request,
                        "AppCoder/registro.html",
                        {"form": formulario}
                  )

def login_view(request):
      if request.user.is_authenticated:
            return render(
                  request,
                  "AppCoder/login.html",
                  {"mensaje": f"Bienvenidx: {request.user.username}"}
            )

      if request.method == "POST":
            formulario = AuthenticationForm(request, data=request.POST)
            if formulario.is_valid():
                  informacion = formulario.cleaned_data
                  usuario = informacion["username"]
                  password = informacion["password"]
                  modelo = authenticate(username=usuario, password=password)
                  
                  if modelo is not None:
                        login(request, modelo)
                        return render(
                              request,
                              "AppCoder/login.html",
                              {"mensaje": f"Bienvenidx {modelo.username}"}
                        )
                  else:
                        mensaje = "Usuario o contraseña incorrectos. Intente nuevamente."
            else:
                  mensaje = "Formulario inválido. Verifique los campos."

      else:
            formulario = AuthenticationForm()
            mensaje = None

      return render(
            request,
            "AppCoder/login.html",
            {"form": formulario, "mensaje": mensaje}
      )

def editar_usuario_view(request):

      if not request.user.is_authenticated:
            return render(
                  request,
                  "AppCoder/login.html",
                  {"form": AuthenticationForm()}
            )

      if request.method == "GET":
            return render(
                  request,
                  "AppCoder/editar_usuario.html",
                  {"form": UserEditionFormulario()}
            )
      else:
            formulario = UserEditionFormulario(request.POST)
            if formulario.is_valid():
                  informacion = formulario.cleaned_data
                  user = request.user
                  user.email = informacion["email"]
                  user.username = informacion["username"]
                  user.save()

                  return render(
                  request,
                  "AppCoder/edicion_success.html",
                  {"mensaje": f"Sus cambios fueron guardados exitosamente."}
                  )
            else:
                  return render(
                  request,
                  "AppCoder/editar_usuario.html",
                  {"form": formulario}
                  )

def edicion_exitosa(request):
      return render(
            request,
            "AppCoder/edicion_success.html",
            {"mensaje": f"Sus cambios fueron guardados exitosamente."}
      )
class CustomPasswordChangeForm(PasswordChangeForm):
      error_messages = {
            'password_incorrect': _('La contraseña actual es incorrecta.'),
            'password_mismatch': _('Las contraseñas no coinciden.'),
            'password_common': _('La contraseña no puede ser una contraseña común.'),
            'password_too_short': _('La contraseña debe tener al menos 8 caracteres.'),
            'password_entirely_numeric': _('La contraseña no puede ser completamente numérica.'),
      }

      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                  field.help_text = ""
class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):
      template_name = "AppCoder/cambiar_contrasenia.html"
      success_url =  "edicion_exitosa"
      form_class = CustomPasswordChangeForm

      def form_invalid(self, form):
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
      
      def get_form(self):
            form = super().get_form()
            form.fields['old_password'].label = _('Contraseña Actual')
            form.fields['new_password1'].label = _('Nueva Contraseña')
            form.fields['new_password2'].label = _('Confirmar Nueva Contraseña')
            return form