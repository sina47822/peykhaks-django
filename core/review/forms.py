from django import forms
from .models import ProductReviewModel
from product.models import Product, ProductStatusType

class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReviewModel
        fields = ['name' , 'product','rate', 'description', 'email']
        error_messages = {
            'description': {
                'required': 'فیلد توضیحات اجباری است',
            },
            'email': {
                'required': 'فیلد ایمیل اجباری است',
            },
        }
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')

        # Check if the product exists and is published
        try:
            Product.objects.get(id=product.id)
        except Product.DoesNotExist:
            raise forms.ValidationError("این محصول وجود ندارد")

        return cleaned_data