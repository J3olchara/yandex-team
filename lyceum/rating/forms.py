from django import forms

from rating import models


class EvaluationForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = models.Evaluation
        fields = ('value',)
        widgets = {'value': forms.NumberInput()}
