from collections.abc import Mapping
from django import forms
from django.forms import ModelForm
import datetime

class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Loop through each field in the form

        for field_name, field in self.fields.items():
            # Check if the field is a CharField, EmailField, etc. (text input fields)
            # if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
            if field.widget:
                # Add the Bootstrap 'form-control' class to the field's widget
                field.widget.attrs.update({"class": "form-control"})


# Heredar de BootstrapForm permite usar los widgets de html de bootstrap en vez de los de django :3
class registerForm(BootstrapForm):
    email = forms.CharField( label="Email")
    contraseña = forms.CharField( label="Contraseña")
    fecha_de_nacimiento = forms.DateField(label="Fecha de nacimiento", widget=forms.DateInput(attrs={'type': 'date'}),)
    nombre = forms.CharField( label="Nombre")
    numero_salud = forms.IntegerField(label="RUPS")