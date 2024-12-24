from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponseRedirect
from product.forms import ProductAdminForm
from product.models import Product, Category, StandardAASHTO, StandardASTM, StandardISIRI, Standards, Tags , ProductMedia ,ProductSpecification, ProductSEO,TagsSEO,CategorySEO,PriceList
from product.models import ProductCategoryModel, WishlistProductModel, PageConfig, PageConfigProduct
from .utils import export_products_to_excel, import_products_from_excel
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields

from product.resources import CombinedStandardsResource
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class ImportExcelForm(forms.Form):
    excel_file = forms.FileField()

# تعریف منابع (resources) برای مدل‌ها
class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id','title', 'slug', 'description', 'summery','price','offer_price','image', 'category','status', 'tags',  'publish_date', 'author', 'total_views', 'is_active','stock','standard','size','guarantee','time_to_bring')

class ProductImagesInline(admin.StackedInline):
    model = ProductMedia  
class ProductSpecificationInline(admin.StackedInline):
    model = ProductSpecification
class TagSEOInline(admin.StackedInline):
    model = TagsSEO
    can_delete = False
class CatSEOInline(admin.StackedInline):
    model = CategorySEO
    can_delete = False
class SEOInline(admin.StackedInline):
    model = ProductSEO
    can_delete = False

class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
    list_display = ('id','title','categories' ,'price', 'offer_price','is_active','stock' )
    list_filter = ('create_date',)
    search_fields = ['title', 'description']
    list_editable = ('price', 'offer_price', 'is_active', 'stock' ,'categories')  # Fields editable directly from the list view
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImagesInline, ProductSpecificationInline, SEOInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.import_excel, name='product_import_excel'),
            path('export-excel/', self.export_excel, name='product_export_excel'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_buttons'] = True  # Flag for displaying buttons
        return super().changelist_view(request, extra_context=extra_context)

    def import_excel(self, request):
        if request.method == "POST":
            form = ImportExcelForm(request.POST, request.FILES)
            if form.is_valid():
                import_products_from_excel(form.cleaned_data['excel_file'])
                self.message_user(request, "Products imported successfully!")
                return redirect("..")
        else:
            form = ImportExcelForm()
        return render(request, "admin/import_excel.html", {"form": form})

    def export_excel(self, request):
        return export_products_to_excel()
admin.site.register(Product, ProductAdmin)

# @admin.register(Product)
# class ProductAdmin2(ImportExportModelAdmin):
#     resource_class = ProductResource
#     form = ProductAdminForm
#     date_hierarchy = 'create_date'
#     list_display = ('id','title','categories' ,'price', 'offer_price','is_active','stock' )
#     list_filter = ('create_date', )
#     list_editable = ('price', 'offer_price', 'is_active', 'stock' ,'categories')  # Fields editable directly from the list view
#     search_fields = ['title', 'description',]
#     prepopulated_fields = {'slug': ('title',)}
#     inlines = [ProductImagesInline ,ProductSpecificationInline,SEOInline] 
    
#     def display_category(self, obj):
#         return ", ".join(category.name for category in obj.categories.all())
#     display_category.short_description = 'categories'
# admin.site.register(Product, ProductAdmin2)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name' ,'parent')
    search_fields = ['name', 'parent']
    inlines = [CatSEOInline] 
admin.site.register(Category,CategoryAdmin)

class TagsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    inlines = [TagSEOInline] 
admin.site.register(Tags,TagsAdmin)

admin.site.register(PriceList)

class StandardsAdmin(ImportExportModelAdmin):
    resource_class = CombinedStandardsResource
    list_display = ('id','title', 'slug' )
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Standards,StandardsAdmin)
admin.site.register(StandardISIRI)
admin.site.register(StandardASTM)
admin.site.register(StandardAASHTO)

@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_date")

@admin.register(WishlistProductModel)
class WishlistProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")

class PageConfigAdminForm(forms.ModelForm):
    class Meta:
        model = PageConfig
        fields = '__all__'
        widgets = {
            'created_at': AdminJalaliDateWidget,  # ویجت جلالی برای انتخاب تاریخ
        }

    
class PageConfigProductInline(admin.TabularInline):
    form = PageConfigAdminForm
    model = PageConfigProduct
    extra = 1  # تعداد فیلدهای اضافی برای هر محصول جدید که به صورت پیش‌فرض نمایش داده می‌شود
    autocomplete_fields = ('product',)  # اضافه کردن قابلیت جستجوی محصول
    readonly_fields = ('price','offer_price','total_price',)

    # نمایش قیمت اصلی محصول
    def price(self, instance):
        if instance.product:
            price = int(instance.product.price)
            formatted_price = f"{price:,.0f}"  # Add comma as thousand separator
            return f"{formatted_price} تومان" 
        return 0
    price.short_description = 'Price'

    # نمایش قیمت تخفیف خورده محصول
    def offer_price(self, instance):
        if instance.product:
            offer_price =  int(instance.product.offer_price) if instance.product.offer_price else 0  # قیمت تخفیف خورده
            formatted_price = f"{offer_price:,.0f}"  # Add comma as thousand separator
            return f"{formatted_price} تومان"   
        return 0
    offer_price.short_description = 'Offer Price'

    def total_price(self, instance):
        if instance.product:
            price = instance.product.offer_price if instance.product.offer_price and instance.product.offer_price < instance.product.price else instance.product.price
            total_price = int(price * instance.quantity)
            # Format the number with commas for better readability
            formatted_price = f"{total_price:,.0f}"  # Add comma as thousand separator
            return f"{formatted_price} تومان"    
        return 0
    total_price.short_description = 'Total Price'
    
@admin.action(description="copy items")
def duplicate_items(modeladmin, request, queryset):
    for obj in queryset:
        # Retrieve all related PageConfigProduct objects
        original_items = PageConfigProduct.objects.filter(page_config=obj)  # Use related_name to fetch related products

        # Create a new PageConfig object
        obj.pk = None  # Reset primary key to create a new instance
        obj.slug = None  # Ensure a unique slug
        obj.page_name = f"{obj.page_name} (Copy)"  # Rename for clarity
        obj.save()  # Save the new PageConfig object

        for item in original_items:
            # Create a new PageConfigProduct instance for the copied PageConfig
            new_item = PageConfigProduct(
                product=item.product,  # Copy the product
                quantity=item.quantity,  # Copy the quantity
                page_config=obj  # Link to the new PageConfig
            )
            new_item.save()  

class PageConfigAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'slug', 'last_update')  # فیلدهایی که در لیست نمایش داده می‌شوند
    inlines = [PageConfigProductInline]  # نمایش محصولات و تعداد آنها در بخش PageConfig
    actions = [duplicate_items]

admin.site.register(PageConfig, PageConfigAdmin)