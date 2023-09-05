from django import forms

class Report(forms.Form):
    disease = forms.CharField(label="Nombre de tu enfermedad")
    diagnosis_place = forms.CharField(label="Lugar de dignóstico")
    #diagnosis_date = forms.DateField(input_formats=,label="fecha de diagnosis")
