from django.db import models
#from ckeditor.fields import RichTextField
from app.usuario.models import Usuario

# Create your models here.

class TipoPublicacion(models.Model):
    tipo_publicacion = models.CharField('Tipo de Publicacion',max_length=50, blank = False, null = False)
    
    class Meta:
        verbose_name = 'Tipo de Publicacion'
        verbose_name_plural = 'Tipos de Publicacion'

    def __str__(self):
        return self.tipo_publicacion

    #1 Imagen
    #2 Video
    #3 Texto
class Publicacion(models.Model):
    archivo = models.FileField('Tipo de Archivo', upload_to='archivo_publicacion/', max_length = 100,
                               blank = True, null = True, default='')
    texto_publicacion = models.TextField('Texto de Publicacion', blank = True, null = True)
    tipo_publicacion = models.ForeignKey(TipoPublicacion, on_delete=models.CASCADE)
    fecha_hora_creacion = models.DateTimeField('Fecha de Creacion', auto_now = False, auto_now_add = True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.BooleanField('Publicacion Activa/Publicacion Eliminada',default = True)

    class Meta:
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-id']

    def __str__(self):
        return "{0},{1}".format(self.usuario, self.texto_publicacion)

class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    #usuario que hace el comentario 
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField('Comentario Realizado')
    fecha_hora_creacion = models.DateTimeField(auto_now = True, auto_now_add = False)
    estado = models.BooleanField('Comentario Activo/Comentario Eliminado',default = True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'


    def __str__(self):
        return "{0},{1}".format(self.usuario, self.comentario)

class Like(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return "{0},{1}".format(self.publicacion, self.usuario)


class Dislike(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Dislike'
        verbose_name_plural = 'Dislikes'

    def __str__(self):
        return "{0},{1}".format(self.publicacion, self.usuario)

    
    

     

