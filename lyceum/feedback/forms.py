from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(
        label='Как к вам обращаться?',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Ваше имя',
            }
        ),
    )

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

    files = forms.FileField(  # type: ignore[assignment]
        label='Приложенные файлы',
        help_text='Приложите файлы',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
