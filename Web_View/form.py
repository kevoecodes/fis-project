# import form class from django
from django import forms

from Fields_Management.models import StudentApplication


# import GeeksModel from models.py
# from .models import GeeksMo


# create a ModelForm
class StudentApplicationForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = StudentApplication
        fields = ['student', 'file', 'field']

