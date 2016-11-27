# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Report


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    id = forms.IntegerField()


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['rating', 'price','id','note']