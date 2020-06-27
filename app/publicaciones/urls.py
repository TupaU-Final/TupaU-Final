from django.urls import path, re_path
from .views import AgregarPublicacion, eliminar_publicacion, AgregarComentario

urlpatterns = [
    path('agregar_publicacion/', AgregarPublicacion.as_view(), name = 'agregar_publicacion'),
    path('eliminar_publicacion/<int:id>', eliminar_publicacion, name = 'eliminar_publicacion'),
    path('agregar_comentario/', AgregarComentario.as_view(), name = 'agregar_comentario'),
     
]   