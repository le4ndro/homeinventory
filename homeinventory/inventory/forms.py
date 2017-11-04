from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from homeinventory.inventory.models import Category, Location


class UserRegistrationForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ItemAttachmentForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput)
    upload = forms.FileField(widget=forms.ClearableFileInput(
                                                attrs={'multiple': True}))


class PhotoAttachmentForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput)
    upload = forms.FileField(widget=forms.ClearableFileInput(
                                                attrs={'multiple': True}))


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'description')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
