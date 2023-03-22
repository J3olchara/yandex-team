from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms

from authorisation.models import UserProxy


class EditProfile(UserChangeForm):

    birthday = forms.DateField(
        label='День рождения',
        widget=forms.DateInput(),
    )

    def __init__(self, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field not in ['email']:
                self.fields[field].required = False
        del self.fields['password']
        self.fields['username'].disabled = True
        self.fields['birthday'].widget.attrs['value'] = args[1]['birthday']

    def save(self, commit: bool = ...):
        self.instance = User.objects.get(
            username=self.cleaned_data['username']
        )
        self.instance.first_name = self.cleaned_data['first_name']
        self.instance.second_name = self.cleaned_data['last_name']
        self.instance.email = self.cleaned_data['email']
        self.instance.profile.birthday = self.cleaned_data['birthday']
        self.instance.profile.save()
        self.instance.save()

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
