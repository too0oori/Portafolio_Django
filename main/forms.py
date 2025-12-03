from django import forms
from .models import Contacto


class ContactoForm(forms.ModelForm):
    """Formulario de contacto"""
    
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu nombre',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu correo electrónico',
                'required': True
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe tu mensaje',
                'required': True
            }),
        }
        labels = {
            'nombre': 'Nombre *',
            'email': 'Correo electrónico *',
            'mensaje': 'Mensaje *',
        }