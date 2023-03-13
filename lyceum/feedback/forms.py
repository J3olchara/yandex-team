from django import forms


class FeedbackForm(forms.Form):
    email = forms.EmailField(
        label='Адрес электронной почты',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Введите ваш email',
            }
        ),
    )

    text = forms.CharField(
        label='Вопрос',
        required=True,
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Опишите вопрос',
            }
        ),
    )
