from django.contrib import admin
from review.models import ProductReviewModel

# Register your models here.
class ProductReviewModelAdmin(admin.ModelAdmin):
    list_display = ('name' ,'email','updated_date')
    search_fields = ['name' ,'email']

admin.site.register(ProductReviewModel,ProductReviewModelAdmin)
