from django import forms
from django.forms import ModelForm, Textarea, DateInput

from homeinventory.inventory.models import Category, Location, Item, ItemLoan


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


class ItemLoanForm(ModelForm):
    item_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = ItemLoan
        fields = ('who', 'when', 'why', 'expected_return_date')
        widgets = {
            'why': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
