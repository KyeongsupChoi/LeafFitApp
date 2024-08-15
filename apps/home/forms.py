# -*- encoding: utf-8 -*-

from django import forms
from .models import RepMax


class WendlerForm(forms.ModelForm):
    """Form for the image model"""
    weight = forms.IntegerField()

    class Meta:

        fields = ('weight',)
        model = RepMax


