from collections.abc import Mapping
from django import forms
from django.forms import ModelForm
import datetime
from persistencia.reportes_dbops import get_input_data
pack = lambda li: ((field, field) for field in li)
sexo = pack(["Sexo","F", "M"])

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
class ReportForm(BootstrapForm):
    disease = forms.CharField(label="Enfermedad")
    municipio = forms.CharField( label="Municipio")
    # municipio = forms.ChoiceField(choices=municipios ,label="Municipio",widget=forms.Select(attrs={'class': 'form-control'}))
    barrio = forms.CharField( label="Barrio")
    sexo_paciente = forms.ChoiceField(choices=sexo, label="Sexo Paciente")
    edad_paciente = forms.IntegerField(label="Edad Paciente")
    # barrio = forms.ChoiceField(choices=barrios ,label="Barrio",widget=forms.Select(attrs={'class': 'form-control'}))
    diagnosis_place = forms.CharField(label="Lugar de diagnóstico")
    diagnosis_date = forms.DateField(initial=datetime.date.today().strftime("%Y-%m-%d"))
    diagnosis_validator = forms.CharField(label="Comprobante de diagnóstico")
