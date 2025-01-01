from django import forms
from .models import ProductReviewModel, PostReviewModel
from product.models import Product, ProductStatusType
from website.models import Post

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
    


class SubmitPostReviewForm(forms.ModelForm):
    class Meta:
        model = PostReviewModel
        fields = ['name', 'post', 'rate', 'description', 'email']
        error_messages = {
            'description': {
                'required': 'فیلد توضیحات اجباری است',
            },
            'email': {
                'required': 'فیلد ایمیل اجباری است',
            },
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
                'aria-label': 'First name',
                'id': 'inputName',  # example ID
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل',
                'id': 'inputEmail4',
            }),
            'rate': forms.Select(attrs={
                'class': 'form-select',
                'id': 'inputState2',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'دیدگاه خود را بنویسید',
                'rows': '3',
                'id': 'exampleFormControlTextarea1',
            }),
            # 'post' can be hidden or excluded from rendering if you pass the post.id manually
            # in your template as a hidden field
        }

    def clean(self):
        """
        Validate that the chosen Post actually exists.
        """
        cleaned_data = super().clean()
        post = cleaned_data.get('post')
        if not post:
            raise forms.ValidationError("پست انتخاب نشده است!")
        # Ensure the post really exists (should be valid if `post` is a valid foreign key).
        try:
            Post.objects.get(pk=post.id)
        except Post.DoesNotExist:
            raise forms.ValidationError("این پست وجود ندارد")

        return cleaned_data