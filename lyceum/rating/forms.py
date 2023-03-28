from django import forms

from . import models


class EvaluationForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = models.Evaluation
        fields = ('value',)
        widgets = {'value': forms.NumberInput()}
