from django import forms
from django.db.models import fields
from django.forms import widgets
from . import models


class AddProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['name', 'Address', 'city', 'state', 'pincode']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'Address': forms.TextInput(attrs={'class': 'form-control'}),
                   'city': forms.TextInput(attrs={'class': 'form-control'}),
                   'state': forms.TextInput(attrs={'class': 'form-control'}),
                   'pincode': forms.NumberInput(attrs={'class': 'form-control'}),
                   }
