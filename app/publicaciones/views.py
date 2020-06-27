from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.views.generic import CreateView, DeleteView, UpdateView
from .models import Publicacion, Comentario, Like
from .forms import FormAgregarPublicacion, FormAgregarComentario, FormLike
from app.amigos.models import Friend  
from app.usuario.models import Usuario  
from app.chat.models import Thread

@login_required(login_url='/login/')
def inicio(request):
    comentario = Comentario.objects.filter(estado = True) 
    solicitudes = Friend.objects.filter(status = 'requested', friend_id = request.user.id)
    usuario_solicitud = Usuario.objects.all()
    amigos = Friend.objects.filter(status = 'friend', friend_id = request.user.id) | Friend.objects.filter(status = 'friend', user_id = request.user.id)
    chats = Thread.objects.by_user(request.user.id)

    publicacion = extraer_publicacion_amigos(request, amigos)
                
    datos = {
        'publicacion': publicacion,
        'comentario': comentario,
        'solicitudes': solicitudes,
        'usuario_solicitud': usuario_solicitud,
        'amigos':amigos,
        'chats': chats
    }
    
    return render(request,'inicio.html',datos)

@login_required(login_url='/login/')
def extraer_publicacion_amigos(request, amigos):
    publicacion_amigos = Publicacion.objects.filter(
                    estado = True, usuario = request.user.id)
    for amigos in amigos :
        if amigos.user_id != request.user.id or amigos.friend_id != request.user.id:
            if amigos.user_id and amigos.friend_id:
                
                publicacion_amigos |= Publicacion.objects.filter(
                    estado = True, usuario = amigos.user_id) | Publicacion.objects.filter(
                    estado = True, usuario = amigos.friend_id)  

            elif amigos.user_id:

                publicacion_amigos |= Publicacion.objects.filter(
                    estado = True, usuario = amigos.user_id)
            else:
                publicacion_amigos |= Publicacion.objects.filter(
                    estado = True, usuario = amigos.friend_id)
        else: 
            return None
    
    return publicacion_amigos

class AgregarPublicacion(LoginRequiredMixin, CreateView):
    model = Publicacion
    form_class = FormAgregarPublicacion
    template_name = 'inicio.html'
    success_url = reverse_lazy('inicio')
    login_url = 'login'

@login_required(login_url='/login/')
def eliminar_publicacion(request, id):
    publicacion = Publicacion.objects.get(id = id)
    publicacion.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AgregarComentario(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = FormAgregarComentario
    template_name = 'inicio.html'
    login_url = 'login'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
        else: 
            return redirect('inicio')
