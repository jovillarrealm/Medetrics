from collections.abc import Mapping
from django import forms
from django.forms import ModelForm
import datetime
from persistencia.reportes_dbops import get_input_data

pack = lambda li: ((field, field) for field in li)
sexo = [
    ('F', 'Femenino'),
    ('M', 'Maculino'),        
]

enfermedad_choices = [
    ('COVID-19', 'COVID-19'),
    ('Influenza', 'Influenza'),        
    ('Dengue', 'Dengue'),
    ('Alzheimer', 'Alzheimer'),
    ('VIH', 'VIH'),
]

diagnosis_place_choices = [
    ('Casa', 'Casa'),
    ('Hospital', 'Hospital'),
    ('Cento medico', 'Centro Medico'),    
]

estrato_choices = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
]

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

    disease = forms.ChoiceField(choices=enfermedad_choices, label="Enfermedad")
    municipio = forms.CharField(label="Municipio")
    # municipio = forms.ChoiceField(choices=municipios ,label="Municipio",widget=forms.Select(attrs={'class': 'form-control'}))
    barrio = forms.CharField( label="Barrio")
    edad_paciente = forms.IntegerField(label="Edad Paciente")
    estrato= forms.ChoiceField(choices=estrato_choices, label="Estrato del paciente")
    sexo_paciente = forms.ChoiceField(choices=sexo, label="Sexo Paciente")
    # barrio = forms.ChoiceField(choices=barrios ,label="Barrio",widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_sintomas = forms.DateField(label="Fecha inicio de sintomas", widget=forms.DateInput(attrs={'type': 'date'}),)
    diagnosis_date = forms.DateField(label="Fecha de diagnostico", widget=forms.DateInput(attrs={'type': 'date'}),)
    diagnosis_place = forms.ChoiceField(choices=diagnosis_place_choices, label="Lugar de diagnostico")
    diagnosis_validator = forms.CharField(label="Comprobante de diagnóstico")
    numero_salud = forms.IntegerField(label= "", widget=forms.HiddenInput())
    
    