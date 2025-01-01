from django.contrib import admin
from review.models import ProductReviewModel
from review.models import PostReviewModel

# Register your models here.
class ProductReviewModelAdmin(admin.ModelAdmin):
    list_display = ('name' ,'email','updated_date')
    search_fields = ['name' ,'email']

admin.site.register(ProductReviewModel,ProductReviewModelAdmin)

@admin.register(PostReviewModel)
class PostReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'rate', 'status', 'created_date')
    list_filter = ('status', 'rate')
    search_fields = ('name', 'post__title')