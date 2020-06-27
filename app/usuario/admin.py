from django.contrib import admin
from .models import TipoUsuario, Genero, Usuario

# Register your models here.
admin.site.register(TipoUsuario)
admin.site.register(Genero)
admin.site.register(Usuario)

