from django.contrib import admin
from .models import TipoPublicacion, Publicacion, Comentario, Like, Dislike


class TipoPublicacionAdmin(admin.ModelAdmin):
    search_fields = ['tipo_publicacion']
    list_display = ('tipo_publicacion',)

class ComentarioAdmin(admin.ModelAdmin):
    search_fields = ['comentario']
    list_display = ('comentario',)

class PublicacionAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('usuario','archivo', 'estado','fecha_hora_creacion','tipo_publicacion')

admin.site.register(TipoPublicacion, TipoPublicacionAdmin)
admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(Comentario, ComentarioAdmin)
