# -*- encoding: utf-8 -*-

from django import forms
from .models import RepMax
from .models import WendlerPlan


class WendlerForm(forms.ModelForm):
    """Form for the image model"""
    weight = forms.IntegerField()

    class Meta:

        fields = ('weight',)
        model = RepMax



class WendlerPlanForm(forms.ModelForm):
    class Meta:
        model = WendlerPlan
        fields = ['name', 'weight', 'exercise_data']
