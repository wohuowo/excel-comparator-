from dataclasses import fields
from django import forms
from .models import ExcelFiles


class ExcelUpload(forms.ModelForm):
    class Meta:
        model = ExcelFiles
        fields = ['title', 'excel']
