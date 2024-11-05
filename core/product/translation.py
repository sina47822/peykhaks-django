from modeltranslation.translator import register, TranslationOptions
from .models import (
    ProductCategoryModel, Category, Tags, Product, 
    ProductSpecification, ProductSEO, 
    TagsSEO, CategorySEO, PriceList
)


@register(ProductCategoryModel)
class ProductCategoryModelTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Tags)
class TagsTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 
        'summery', 'price', 'offer_price', 
    )

@register(ProductSpecification)
class ProductSpecificationTranslationOptions(TranslationOptions):
    fields = ('name', 'value',)

@register(ProductSEO)
class ProductSEOTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(TagsSEO)
class TagsSEOTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(CategorySEO)
class CategorySEOTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(PriceList)
class PriceListTranslationOptions(TranslationOptions):
    fields = ('title', 'upload_date',)
