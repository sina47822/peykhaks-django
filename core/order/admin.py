from django.contrib import admin
from django import forms
from .forms import OrderForm
from .models import Order, OrderItem, Customer
from django.utils.safestring import mark_safe
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from jalali_date import date2jalali
from product.models import Product
from django.urls import reverse

class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'created_at': AdminJalaliDateWidget,  # ویجت جلالی برای انتخاب تاریخ
        }

class OrderItemInline(admin.TabularInline):
    form = OrderAdminForm  # استفاده از فرم سفارشی
    model = OrderItem
    extra = 0  # تعداد ردیف‌های خالی برای اضافه کردن
    autocomplete_fields = ('product',)  # اضافه کردن قابلیت جستجوی محصول
    # اضافه کردن فیلد قیمت کل به لیست فیلدها
    readonly_fields = ('price','offer_price','total_price',)

    # نمایش قیمت اصلی محصول
    def price(self, instance):
        if instance.product:
            return int(instance.product.price)  # قیمت اصلی محصول
        return 0
    price.short_description = 'Price'

    # نمایش قیمت تخفیف خورده محصول
    def offer_price(self, instance):
        if instance.product:
            return int(instance.product.offer_price) if instance.product.offer_price else 0  # قیمت تخفیف خورده
        return 0
    offer_price.short_description = 'Offer Price'

    def total_price(self, instance):
        if instance.product:
            price = instance.product.offer_price if instance.product.offer_price and instance.product.offer_price < instance.product.price else instance.product.price
            return int(price * instance.quantity)
        return 0
    total_price.short_description = 'Total Price'
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('factor_number', 'customer', 'created_at_p','update_at_p')
    search_fields = ['customer__name']
    change_form_template = 'admin/order/order/change_form.html'
    
    def generate_pdf_link(self, obj):
        """Generate a link to download the PDF of the order"""
        try:
            url = reverse('order:order_generate_pdf', args=[obj.id])  # Reverse the URL for the PDF generation
            return mark_safe(f'<a href="{url}" target="_blank">Download PDF</a>')
        except Exception as e:
            return f"Error generating link: {str(e)}"

    generate_pdf_link.short_description = 'Download Invoice (PDF)'

    def created_at_p(self, obj):
        return date2jalali(obj.created_at).strftime('%Y/%m/%d')    
    created_at_p.short_description = 'تاریخ ایجاد (هجری شمسی)'
    
    def update_at_p(self, obj):
        return date2jalali(obj.updated_at).strftime('%Y/%m/%d')    
    update_at_p.short_description = 'تاریخ ایجاد (هجری شمسی)'
    
    def save_model(self, request, obj, form, change):
        obj.save()
        
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Get the total price for the current object and pass it to the template
        order = self.model.objects.get(id=object_id)
        extra_context = extra_context or {}
        extra_context['total_price'] = order.calculate_total_price
        return super().change_view(request, object_id, form_url, extra_context)

admin.site.register(Order, OrderAdmin)
admin.site.register(Customer)
