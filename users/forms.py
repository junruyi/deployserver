from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField

from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=('Username'),max_length=100)
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput, max_length=100,
        strip=False)
    captcha = CaptchaField()


class UserCreateUpdateForm(forms.ModelForm):
    class Meta:
        module = User
        fields = [ 'username', 'name', 'email','phone', 'role' ]
        help_texts = {
            'username': '用户名',
            'name': '姓名',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        module = User
        fields = ['username', 'name', 'email', 'phone']


class UserPasswordForm(forms.Form):
    old_password = forms.CharField(
        max_length=128, widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        min_length=5, max_length=128, widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        min_length=5, max_length=128, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(UserPasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.instance.check_password(old_password):
            raise forms.ValidationError(_('Old password error'))
        return old_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']

        if new_password != confirm_password:
            raise forms.ValidationError(_('Password does not match'))
        return confirm_password

    def save(self):
        password = self.cleaned_data['new_password']
        self.instance.set_password(password)
        self.instance.save()
        return self.instance


