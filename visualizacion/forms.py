from collections.abc import Mapping
from django import forms
from django.forms import ModelForm
import datetime


from persistencia.reportes_dbops import get_input_data

mock_data = get_input_data()

enfermedades = mock_data[0]
municipios = mock_data[1]
barrios= mock_data[2]




class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Loop through each field in the form
        for field_name, field in self.fields.items():
            # Check if the field is a CharField, EmailField, etc. (text input fields)
            #if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
            if field.widget:
                # Add the Bootstrap 'form-control' class to the field's widget
                field.widget.attrs.update({'class': 'form-control'})

# Heredar de BootstrapForm permite usar los widgets de html de bootstrap en vez de los de django :3
# Se podría configurar un widget de bootstrap correspondiente al tipo de Field
#  
class QueryForm(BootstrapForm):
    disease = forms.ChoiceField(
        choices=enfermedades,
    )
    
    municipio = forms.ChoiceField(
        choices=municipios,
    )
    
    barrio = forms.ChoiceField(
        choices=barrios,
    )

    diagnosis_date = forms.DateField(
        initial=datetime.date.today().strftime("%Y-%m-%d"),
    )

