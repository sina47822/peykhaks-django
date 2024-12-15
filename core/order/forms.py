from django import forms
from .models import Order, OrderItem
from product.models import Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
            
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=forms.CheckboxSelectMultiple)
    quantities = forms.CharField()

    def save(self, commit=True):
        order = super().save(commit=False)
        order.save()

        product_ids = self.cleaned_data['products']
        quantities = self.cleaned_data['quantities'].split(',')

        for product_id, quantity in zip(product_ids, quantities):
            OrderItem.objects.create(
                order=order,
                product=Product.objects.get(id=product_id),
                quantity=int(quantity)
            )

        return order