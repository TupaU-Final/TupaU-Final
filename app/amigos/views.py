import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from django.contrib import messages
from app.usuario.models import Usuario

from .serializers import NotificationSerializer
from .models import *
from django.urls import reverse_lazy

class FindFriendsListView(LoginRequiredMixin, ListView):
    model = Friend
    context_object_name = 'usuario'
    template_name = "amigos/buscar_amigos.html"
    login_url = 'login'

    def get_queryset(self):
        # Esta vaina lista los amigos actuales
        current_user_friends = self.request.user.friends.values('id')
        # Esta lista a los que les ha enviado la solicitu
        sent_request = list(Friend.objects.filter(user=self.request.user).values_list('friend_id', flat=True))
        # Y esta de aqui hace un listado de todos, excluyendo a tus amigos y a los que le enviaste la solicitud
        users = Usuario.objects.exclude(id__in=current_user_friends).exclude(id__in=sent_request).exclude(id=self.request.user.id)
        
        return users
    
    def post(self, request, *args, **kwargs):
        search_user = self.request.POST.get('search_user')

        current_user_friends = self.request.user.friends.values('id')
        # Esta lista a los que les ha enviado la solicitu
        sent_request = list(Friend.objects.filter(user=self.request.user).values_list('friend_id', flat=True))
        
        if search_user:
            users = Usuario.objects.filter(
                Q(nombre__icontains = search_user) |
                Q (apellido__icontains = search_user) |
                Q(username__icontains = search_user) |
                Q(email__icontains = search_user)
            ).exclude(id__in = current_user_friends
            ).exclude(id__in = sent_request
            ).exclude(id=self.request.user.id
            ).distinct()

        return render(request, 'amigos/buscar_amigos.html', {'usuario':users})


@login_required(login_url='/login/')
def send_request(request, username=None):
    if username is not None:
        friend_user = Usuario.objects.get(username=username)
        friend = Friend.objects.create(user=request.user, friend=friend_user)
        notification = CustomNotification.objects.create(type="friend", recipient=friend_user, actor=request.user, verb="sent you friend request")
        channel_layer = get_channel_layer()
        channel = "notifications_{}".format(friend_user.username)
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",  # method name
                "command": "new_notification",
                "notification": json.dumps(NotificationSerializer(notification).data)
            }
        )
        data = {
            'status': True,
            'message': "Request sent.",
        }

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        pass


@login_required(login_url='/login/')
def accept_request(request, friend=None):
    if friend is not None:
        friend_user = Usuario.objects.get(username=friend)
        current_user = request.user
        f = Friend.objects.filter(user=friend_user, friend=current_user, status='requested')[0]
        f.status = "friend"
        f.save()
        CustomNotification.objects.filter(recipient=current_user, actor=friend_user).delete()
        data = {
            'status': True,
            'message': "You accepted friend request",
        }
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def rejected_request(request, friend=None):
    if friend is not None:
        friend_user = Usuario.objects.get(username=friend)
        current_user = request.user
        f = Friend.objects.filter(user=friend_user, friend=current_user, status='requested')[0]
        f.status = "rejected"
        f.save()
        CustomNotification.objects.filter(recipient=current_user, actor=friend_user).delete()
        data = {
            'status': False,
            'message': "You rejected friend request",
        }
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))