from django import forms
from .models import Publicacion,Comentario, Like

class FormAgregarPublicacion(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ('archivo','texto_publicacion','tipo_publicacion','usuario')

        widgets = {
            'archivo': forms.FileInput(
                attrs= {
                    'class': 'form-control'
                }
            ),
            'texto_publicacion': forms.TextInput(
                attrs= {
                    'class': 'form-control'
                }
            ),
            'tipo_publicacion': forms.HiddenInput(
             attrs= {
                 'class': 'form-control'
                }   
            ),
            'usuario': forms.HiddenInput(
                attrs= {
                    'class': 'form-control'
                }
            )
        } 


class FormAgregarComentario(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('publicacion','usuario','comentario')

        widgets = {
            'publicacion': forms.HiddenInput(
                attrs= {
                    'class': 'form-control'
                }
            ),
            'usuario': forms.HiddenInput(
                attrs= {
                    'class': 'form-control'
                }
            ),
            'comentario': forms.TextInput(
                attrs= {
                    'class': 'form-control'
                }
            )
        }


class FormLike(forms.ModelForm):
    class Meta:
        model = Like
        fields = ('publicacion','usuario')