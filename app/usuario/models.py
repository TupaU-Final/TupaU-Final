from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.urls import reverse, reverse_lazy
# Create your models here.
class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombre, apellido, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico!')
        
        user = self.model(
            username = username,
            email = self.normalize_email(email), 
            nombre = nombre,
            apellido = apellido 
        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,email,nombre, apellido, password):
        user = self.create_user(
            email,
            username=username,            
            nombre=nombre,
            apellido=apellido,
            password=password
        )
        user.usuario_administrador = True
        user.save()
        return user

class TipoUsuario(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Tipo de Usuario', max_length=100, blank=True, null=True, default="Sin Datos")

    def __str__(self):
        return '{} - {}'.format(
            self.id,
            self.nombre
        )


class Genero(models.Model):
    id = models.AutoField(primary_key=True)
    genero = models.CharField(max_length = 15, default="Prefiero no decir")

    def __str__(self):
        return '{}'.format(
            self.genero
        )


class Usuario(AbstractBaseUser):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)
    apellido = models.CharField('Apellido', max_length=150, blank=False, null=False)
    email = models.EmailField('Correo Electrónico', max_length=254, unique=True, blank=False, null=False)
    username = models.CharField('Nombre de Usuario', max_length=50, unique=True, blank=False, null=False)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, default=1)
    
    #Datos que se llenan despues del registro
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', blank=True, null=True)
    foto_perfil = models.ImageField('Foto de Perfil',upload_to='foto_perfil/',
                                height_field=None,width_field=None,
                                max_length=200, blank=False,
                                null=True, default='foto_perfil/avatar.png'
                                )
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, default=1)
    universidad = models.CharField('Universidad',max_length = 150, blank=True, null=True, default='Sin registro')
    carrera = models.CharField('Carrera',max_length = 150, blank=True, null=True, default='Sin registro')
    hobbies = models.CharField('Hobbies',max_length = 150, blank=True, null=True, default='No hay datos')
    situacion_sentimental = models.CharField('Situación Sentimental',max_length = 150,  null=True, default='No hay datos')
    descripcion_breve = models.TextField('Descripción Breve', default = 'No hay datos')
    
    is_active = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager()

    #Campo que diferencia al usuario de los demás
    USERNAME_FIELD = 'email'

    #Campos requeridos
    REQUIRED_FIELDS = ['username','nombre','apellido'] 

    def __str__(self):
        return self.nombre + " " + self.apellido
    

    def has_perm(self, perm, obj = None):
        """Este metodo es llamado por el administrador de Django,
        para otorgar el permiso de entrar al administrador de Django"""
        return True

    def has_module_perms(self, app_label):
        """Tambien es para el administrador de Django, recibe app_label
        que basicamente dice en que aplicacion esta situado nuestro modelo Usuario"""
        return True


    @property
    def is_staff(self):
        #Verifica si el usuario es administrador o no
        return self.usuario_administrador


