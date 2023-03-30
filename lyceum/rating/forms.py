from django import forms

from rating import models


class EvaluationForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = models.Evaluation
        fields = ('value',)
        widgets = {
            'value': forms.NumberInput(
                attrs={
                    'type': 'range',
                    'class': 'form-range mb-5',
                    'step': '1',
                    'min': '0',
                    'max': '5',
                    'value': '5',
                }
            )
        }
