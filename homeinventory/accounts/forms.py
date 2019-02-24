from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class UserRegistrationForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class EditEmailForm(forms.Form):
    """
    A form that lets a user change set their email entering the password
    """
    error_messages = {
        'email_mismatch': "The two email fields didn't match.",
    }
    new_email1 = forms.EmailField(
        label="New email",
    )
    new_email2 = forms.EmailField(
        label="New email confirmation",
    )

    def clean_new_email2(self):
        email1 = self.cleaned_data.get('new_email1')
        email2 = self.cleaned_data.get('new_email2')
        if email1 and email2:
            if email1 != email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )

        return email2
