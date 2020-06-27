from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, View
from app.usuario.forms import FormLogin, FormUser,FormDatosUser, FormEditarHobbies, FormLlenarDatos, FormEditarUsuario
from app.usuario.models import Usuario
from app.publicaciones.models import Publicacion 
from app.publicaciones.models import Comentario 
from app.amigos.models import Friend
# Create your views here.


class Login(FormView):
    template_name = 'usuario/login.html'
    form_class = FormLogin
    success_url = reverse_lazy('inicio')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self,form):
        login(self.request, form.get_user())
        return super(Login,self).form_valid(form)


def logout_usuario(request):
    logout(request)
    return HttpResponseRedirect('/login/') #Mija :v


def terminos_condiciones(request):
    return render(request, 'usuario/terminos.html')


class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = FormUser
    template_name = 'usuario/registro.html'
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario = Usuario(
                nombre = form.cleaned_data.get('nombre'),
                apellido = form.cleaned_data.get('apellido'),
                email = form.cleaned_data.get('email'),
                username = form.cleaned_data.get('username'),
                genero = form.cleaned_data.get('genero')
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()

            return redirect('usuario:registro_exitoso')
        else:
            return render(request, self.template_name,{'form':form})


@login_required(login_url='/login/')
def inicio(request):
    usuario = Usuario.objects.filter(is_active = True)
    return render(request, 'inicio.html', {'usuario':usuario})

@login_required(login_url='/login/')
def perfil_usuario(request, user_id):
    usuario = Usuario.objects.get(id = user_id, is_active = True)
    publicacion_usuario = Publicacion.objects.filter(usuario = user_id, estado = True)
    amigos = Friend.objects.filter(status = 'friend', friend_id = user_id
    ) | Friend.objects.filter(status = 'friend', user_id = user_id)
    comentario = Comentario.objects.all()

    datos_perfil = {
        'usuario':usuario,
        'publicacion': publicacion_usuario,
        'comentario': comentario,
        'amigos': amigos
    }

    return render(request, 'usuario/perfil.html', datos_perfil) 

@login_required(login_url='/login/')
def amigos_usuario(request, user_id):
    usuario = Usuario.objects.get(id = user_id, is_active = True)
    amigos = Friend.objects.filter(status = 'friend', friend_id = user_id
    ) | Friend.objects.filter(status = 'friend', user_id = user_id)

    perfiles_usuario = extraer_perfiles_amigos(request, amigos, user_id)

    datos = {
        'usuario': usuario,
        'amigos':amigos,
        'perfiles_usuario': perfiles_usuario
    }

    return render(request, 'usuario/amigos_usuario.html', datos)

@login_required(login_url='/login/')
def extraer_perfiles_amigos(request, amigos, user_id):
    perfiles_usuario = Usuario.objects.filter(
                    is_active = True, id = user_id)
    for amigos in amigos :
        if amigos.user_id != request.user.id or amigos.friend_id != request.user.id:
            if amigos.user_id and amigos.friend_id:
                
                perfiles_usuario |= Usuario.objects.filter(
                    is_active = True, id = amigos.user_id) | Usuario.objects.filter(
                    is_active = True, id = amigos.friend_id)  

            elif amigos.user_id:

                perfiles_usuario |= Usuario.objects.filter(
                    is_active = True, id = amigos.user_id)
            else:
                perfiles_usuario |= Usuario.objects.filter(
                    is_active = True, id = amigos.friend_id)
        else: 
            return None
    
    return perfiles_usuario

class PerfilUsuario(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'usuario/perfil.html'
    form_class = FormUser
    context_object_name = 'usuario'
    login_url = 'login'

''' class DetallePerfilUsuario(DetailView):
    model = Usuario
    template_name = 'usuario/detalle_perfil.html'
    form_class = FormUser
    context_object_name = 'usuario'  '''

class ActualizarCamposExtras(LoginRequiredMixin,UpdateView):
    model = Usuario
    template_name = 'usuario/llenar_datos.html'
    form_class = FormDatosUser
    success_url = reverse_lazy('usuario:actualizacion_correcta') 
    login_url = 'login'


class ActualizarDatos(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'usuario/editar_perfil.html'
    form_class = FormEditarUsuario
    success_url = reverse_lazy('usuario:actualizacion_correcta')
    login_url = 'login'


class EditarHobbies(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = FormEditarHobbies
    template_name = 'usuario/agregar_info.html'
    success_url = reverse_lazy('usuario:actualizacion_correcta') 
    login_url = 'login'


def registro_exitoso(request):
    return render (request, 'usuario/registro_exitoso.html')

class LlenarDatos(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = FormLlenarDatos
    template_name = 'usuario/modals/agregar_datos.html'
    success_url = reverse_lazy('inicio')
    login_url = 'login'

def actualizacion_correcta(request):
    return render(request, 'usuario/actualizacion_correcta.html')