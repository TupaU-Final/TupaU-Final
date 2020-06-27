"""TupaU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app.usuario.views import Login, logout_usuario
from django.conf import settings
from django.conf.urls.static import static
from app.publicaciones.views import inicio


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('app.usuario.urls','usuario'))),
    path('', include(('app.publicaciones.urls','publicacion'))),
    path('login/',Login.as_view(), name = 'login'),
    path('logout/',logout_usuario,name = 'logout'),
    path('', inicio, name = 'inicio'),
    # Urls de chat
    path('chat/', include('app.chat.urls','chat')),

    # Urls de amigos
    path('amigos/', include('app.amigos.urls','amigos')),

    #Manejo de contraseñas
    path('cambio_contraseña/correcto', auth_views.PasswordChangeDoneView.as_view(template_name='usuario/contraseña/cambiar_contraseña_correcto.html'), 
        name='password_change_done'),

    path('cambiar_contraseña/', auth_views.PasswordChangeView.as_view(template_name='usuario/contraseña/cambiar_contraseña.html'), 
        name='password_change'),


    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 