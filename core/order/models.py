from django.db import models
from product.models import Product
from django.utils.translation import gettext_lazy as _
from jalali_date import date2jalali

class Order(models.Model): 
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)  # automatically updates every time the object is saved
    factor_number = models.CharField(max_length=50)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)

    @property
    def persian_created_at(self):
        return date2jalali(self.created_at).strftime('%Y-%m-%d')

    def __str__(self):
        return 'فاکتور شماره ' + str(self.factor_number)

    @property
    def calculate_total_price(self):
        total = 0
        for item in self.orderitem_set.all():  # Loop through each OrderItem
            if item.product:
                # Calculate the price based on the offer_price if it exists and is less than the regular price
                price = item.product.offer_price if item.product.offer_price and item.product.offer_price < item.product.price else item.product.price
                total += price * item.quantity  # Add the calculated price to the total
        return int(total)
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)
        
    @property
    def total_price(self):
        if self.product:
            # If offer_price exists and is less than price, use offer_price, otherwise use price
            price = self.product.offer_price if self.product.offer_price and self.product.offer_price < self.product.price else self.product.price
            return int(price * self.quantity)
        return 0

    def __str__(self):
        return self.product.title

class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    number = models.CharField(max_length=50)

    def __str__(self):
        return self.name