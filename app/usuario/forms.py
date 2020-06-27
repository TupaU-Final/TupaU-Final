from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from app.usuario.models import Usuario

class FormLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input-form'
        self.fields['password'].widget.attrs['class'] = 'input-form'


#SE DEFINEN ESTOS CAMPOS PORQUE EN MODELO USUARIO NO ESTÁN
class FormUser(forms.ModelForm):
#Formulario de Registro de Usuario
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'input-form',
            'id': 'password1',
            'required': 'required'
        }
    )) 

    password2 = forms.CharField(label = 'Repetir Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'input-form',
            'id': 'password2',
            'required': 'required'
        }
    )) 

    class Meta:
        model = Usuario
        labels = {
            'nombre': 'Nombre:',
            'apellido': 'Apellido:',
            'email': 'Correo Electrónico',
            'username': 'Usuario:',
            'genero': 'Género',
            'fecha_nacimiento': 'Fecha De Nacimiento',
            'foto_perfil': 'Foto de Perfil',
            'tipo_usuario': '¿Qué eres?',
            'universidad': '¿Dónde Estudias?',
            'carrera': '¿Qué estudias?'
        }
        fields = (
        'nombre', 'apellido', 'email','genero','username')

        widgets = {
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'input-form'
                }
            ),
            'apellido': forms.TextInput(
                attrs = {
                    'class': 'input-form'
                }
            ),

            'email': forms.EmailInput(
                attrs = {
                    'class': 'input-form'
                }
            ),
            'genero': forms.Select(
                attrs = {
                    'class': 'form-control',
                    'id': 'inputState'
                }
            ),
            'username': forms.TextInput(
                attrs = {
                    'class': 'input-form'
                }
            )
        }  

    def clean_password2(self):
        #Validacion de la contraseña, cleaned_data es un diccionario que tiene los datos ya limpios
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        
        elif len(password1)<8:
            raise forms.ValidationError('La Contraseña debe tener como mínimo 8 caracteres')

        else:
            return password2
    
    def clean_genero(self):
        genero = str(self.cleaned_data.get('genero'))
        genero_class = self.cleaned_data.get('genero')
        

        """ genero_class es una variable que se crea para retornar la instancia a la
        clase, si retorno "genero" marca error, por eso necesita una instancia
        de la clase """

        if genero=="- - - - - - - -":
            raise forms.ValidationError('Debes Seleccionar un Género')
        else:
            return genero_class

    def save(self, commit = True):
        usuario = super().save(commit = False)
        usuario.set_password(self.cleaned_data['password1'])

        if commit:
            usuario.save()
        else:
            return usuario 
        

class FormDatosUser(forms.ModelForm):
    """Esta clase form es para llenar y validar los datos restantes
    del usuario, que son: tipo_usuario, foto, carrera, universidad, entre otros"""
    class Meta:
        model = Usuario 
        labels = {
            'tipo_usuario':'¿Qué eres?',
            'universidad': '¿Dónde estudias?',
            'carrera': '¿Qué estudias o que deseas estudiar?',
            'foto_perfil':'Elije una foto de perfil'
        }

        fields = ('tipo_usuario','universidad','carrera','foto_perfil')

        widgets = {
            'tipo_usuario': forms.Select(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'universidad': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'carrera': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'foto_perfil': forms.FileInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
        }


class FormLlenarDatos(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('foto_perfil','tipo_usuario', 'fecha_nacimiento', 'universidad', 'carrera')
        
        #Ciclo para los años que se mostratan en el Select
        for i  in range (1958,2021):
            años = []
            años.append(i)
            años = tuple(años)
            

        widgets = {
            'tipo_usuario': forms.Select(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'fecha_nacimiento': forms.SelectDateWidget(
                attrs = {
                    'class': 'form-control'
                },
                
            ),
    }

class FormEditarUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('foto_perfil','tipo_usuario', 'fecha_nacimiento', 'nombre', 'apellido','email', 'username', 'universidad','carrera')

        widgets = {
        'tipo_usuario': forms.Select(
            attrs = {
                'class': 'form-control'
            }
        ),
        'fecha_nacimiento': forms.SelectDateWidget(
            attrs = {
                'class': 'form-control'
            },
            
        ),
    }

class FormEditarHobbies(forms.ModelForm):
    class Meta:
        model = Usuario 
        fields = ('hobbies','situacion_sentimental','descripcion_breve')
