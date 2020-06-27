from django.urls import path
from .views import (RegistrarUsuario, PerfilUsuario, perfil_usuario, ActualizarCamposExtras, 
EditarHobbies, ActualizarDatos, registro_exitoso, LlenarDatos, actualizacion_correcta, amigos_usuario, terminos_condiciones)


urlpatterns = [
    path('registro/', RegistrarUsuario.as_view(), name='registro_usuario'),
    path('perfil/<int:user_id>/', perfil_usuario, name='perfil_usuario'),
    path('detalle_perfil/<int:pk>/', PerfilUsuario.as_view(template_name = 'usuario/detalle_perfil.html'),
        name='detalle_perfil_usuario'),
    path('llenar_datos/<int:pk>/', ActualizarCamposExtras.as_view(), name='llenar_datos'),
    path('editar_perfil/<int:pk>/', ActualizarDatos.as_view(), name='editar_perfil'),
    path('editar_info/<int:pk>', EditarHobbies.as_view(), name='editar_hobbies'),
    path('registro_exitoso/', registro_exitoso, name='registro_exitoso'),
    path('agregar_imagen/<int:pk>', LlenarDatos.as_view(), name='llenar_datos'),
    path('actualizacion_correcta/', actualizacion_correcta, name='actualizacion_correcta'),
    path('usuario_amigos/<int:user_id>', amigos_usuario, name='amigos_usuario'), 
    path('terminos_condiciones/', terminos_condiciones, name='terminos'), 
    
]
