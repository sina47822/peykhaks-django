from django import forms
from django.forms import formset_factory

from .models import  Product
from tinymce.widgets import TinyMCE

class PriceUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['price', 'offer_price']

PriceUpdateFormset = formset_factory(PriceUpdateForm, extra=0)

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
