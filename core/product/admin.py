from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponseRedirect
from product.forms import ProductAdminForm
from product.models import Product, Category, StandardAASHTO, StandardASTM, StandardISIRI, Standards, Tags , ProductMedia ,ProductSpecification, ProductSEO,TagsSEO,CategorySEO,PriceList
from product.models import ProductCategoryModel, WishlistProductModel
from .utils import export_products_to_excel, import_products_from_excel
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields

from product.resources import CombinedStandardsResource

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
