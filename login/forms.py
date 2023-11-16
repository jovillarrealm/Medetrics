from django import forms

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


class LoginForm(BootstrapForm):
    email = forms.EmailField(label='Email')
    contraseña = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class RecuperarForm(BootstrapForm):
    email = forms.EmailField(label='Email')
    nueva_contraseña =  forms.CharField(widget=forms.PasswordInput, label='Nueva contraseña')