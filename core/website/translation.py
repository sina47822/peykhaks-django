from modeltranslation.translator import register, TranslationOptions
from .models import (
    Category, Tags, Post, PostSEO, 
    TagsSEO, CategorySEO, SliderModel, Comment
)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

@register(Tags)
class TagsTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = (
        'title', 'slug', 'desc_1', 'desc_2', 
        'post_summery', 'blog_status'
    )

@register(PostSEO)
class PostSEOTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(TagsSEO)
class TagsSEOTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(CategorySEO)
class CategorySEOTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(SliderModel)
class SliderModelTranslationOptions(TranslationOptions):
    fields = ('title', 'alt',)

@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('name', 'body',)
