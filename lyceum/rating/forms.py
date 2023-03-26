from typing import Any, Optional


from django import forms
from . import models


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = models.Evaluation
        fields = ('value',)
        widgets = {
            'value': forms.NumberInput()
        }
