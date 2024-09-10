from django.contrib import admin
from product.forms import ProductAdminForm
from product.models import Product, Category, StandardAASHTO, StandardASTM, StandardISIRI, Standards, Tags , ProductMedia ,ProductSpecification, ProductSEO,TagsSEO,CategorySEO,PriceList
from product.models import ProductCategoryModel, WishlistProductModel
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields

from product.resources import CombinedStandardsResource


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


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    form = ProductAdminForm
    date_hierarchy = 'create_date'
    list_display = ('id','title' ,'image', 'slug','price', 'offer_price','create_date' )
    list_filter = ('create_date', )
    search_fields = ['title', 'description',]
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImagesInline ,ProductSpecificationInline,SEOInline] 
    
    def display_category(self, obj):
        return ", ".join(category.name for category in obj.categories.all())
    display_category.short_description = 'categories'
admin.site.register(Product, ProductAdmin)

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
