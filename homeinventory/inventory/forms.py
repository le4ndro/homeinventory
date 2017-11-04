from django import forms
from django.forms import ModelForm, Textarea, DateInput
from django.contrib.auth.models import User
from homeinventory.inventory.models import Category, Location, Item


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


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = (
                    'make',
                    'model',
                    'id_number',
                    'purchased_from',
                    'purchased_date',
                    'quantity',
                    'value',
                    'estimated_current_value',
                    'description',
                    'attributes',
                    'notes',
                    'year',
                    'category',
                    'location',
                    'warranty',
                    'warranty_type',
                    'warranty_expiration',
                    'warranty_contact_info'
                 )
        labels = {
            'model': 'Model/Name/Title',
            'description': 'Description/Details',
        }
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
            'attributes': Textarea(attrs={'cols': 80, 'rows': 5}),
            'warranty_contact_info': Textarea(attrs={'cols': 80, 'rows': 5}),
            'notes': Textarea(attrs={'cols': 80, 'rows': 5}),
            'purchased_date': DateInput(),
            'warranty_expiration': DateInput(),
        }
