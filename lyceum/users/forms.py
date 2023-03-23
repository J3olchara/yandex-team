from typing import Any, Dict, Optional, Union

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

# isort: off
from authorisation.models import UserProxy  # noqa: I100

# isort: on


class DateInput(forms.DateInput):
    input_type = 'date'


class EditProfile(UserChangeForm):  # type: ignore[type-arg]
    avatar = forms.FileField(widget=forms.FileInput())

    birthday = forms.DateField(
        label='День рождения',
        widget=DateInput(format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
    )

    def __init__(
        self, data: Optional[Dict[str, Any]], *args: Any, **kwargs: Any
    ) -> None:
        super(EditProfile, self).__init__(data, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control 100'
            if field != 'email':
                self.fields[field].required = False
        del self.fields['password']

    def save(
        self, commit: bool = True, user: Union[UserProxy, Any] = None
    ) -> None:
        user.first_name = self.cleaned_data.get('first_name')
        # print(self.fields['birthday'].widget.__dict__)
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if self.cleaned_data.get('birthday'):
            user.profile.birthday = self.cleaned_data['birthday']
            user.profile.avatar = self.cleaned_data['avatar']
            user.profile.save()
        user.save()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        widgets = {'birthday': DateInput()}
