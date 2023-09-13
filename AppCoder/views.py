from django.http.request import QueryDict
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from AppCoder.models import CrearUsuario, Publicacion, Comentario
from AppCoder.forms import UsuarioForm, PublicacionForm, ComentarioForm, UserCreationFormCustom
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.

def inicio(request):
      publicaciones = Publicacion.objects.all()
      return render(request, "AppCoder/inicio.html", {"publicaciones": publicaciones})


def muro(request):
      publicaciones = Publicacion.objects.all()
      return render(request, "AppCoder/mimuro.html", {"publicaciones": publicaciones})


def hilo(request):
      if request.method == 'POST':
            miFormulario = UsuarioForm(request.POST)
            print(miFormulario)
            if miFormulario.is_valid:
                  informacion = miFormulario.cleaned_data
                  usuario  = CrearUsuario(usuario=informacion['usuario'], contraseña=informacion['contraseña']) 
                  usuario.save()
                  return redirect('Inicio')
      else: 
            miFormulario= UsuarioForm()
      return render(request, "AppCoder/hilo.html", {"miFormulario":miFormulario})


def publicar(request):
      if request.method == 'POST':
            miFormulario = PublicacionForm(request.POST) #aquí mellega toda la información del html
            print(miFormulario)
            if miFormulario.is_valid():   #Si pasó la validación de Django
                  informacion = miFormulario.cleaned_data
                  publicacion = Publicacion(contenido=informacion['contenido'], autor_nombre=informacion['autor_nombre'])
                  publicacion.save()
                  publicaciones = Publicacion.objects.all()
                  return render(request, "AppCoder/mimuro.html", {"publicaciones": publicaciones}) #Vuelvo al mi muro
      else: 
            miFormulario= PublicacionForm() #Formulario vacio para construir el html
      return render(request, "AppCoder/publicar.html", {"miFormulario":miFormulario})


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
                  autor_nombre = comentario_form.cleaned_data['autor_nombre']
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


def login_request(request):
      if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)

            if form.is_valid():
                  usuario = form.cleaned_data.get("username")
                  contraseña = form.cleaned_data.get("password")

                  user = authenticate(username=usuario, password=contraseña)

                  login(request, user)
                  return redirect("Inicio", {"mensaje": f'Bienvenido {user.username}'})
      else:
            form = AuthenticationForm()
      return render(request, "AppCoder/login.html", {"form": form})

def register(request):
      if request.method == "POST":
            form = UserCreationFormCustom(request.POST)

            if form.is_valid():
                  user = form.save()
                  login(request, user)
                  return redirect("Inicio", {"mensaje": f'Bienvenido {user.username}'})
      else:
            form = UserCreationFormCustom()

      return render(request, "AppCoder/registro.html", {"form": form})