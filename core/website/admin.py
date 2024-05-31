from django.contrib import admin
from website.models import Post, Category, SliderModel, Tags, PostSEO,TagsSEO,CategorySEO
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils.html import format_html


# تعریف منابع (resources) برای مدل‌ها
class PostResource(resources.ModelResource):
    class Meta:
        model = Post
        fields = ('image','id','title', 'slug', 'desc_1', 'desc_2', 'post_summery', 'categories', 'tags',  'publish_date', 'author', 'total_views', 'blog_status')


def duplicate_selected_posts(modeladmin, request, queryset):
    for post in queryset:
        post.pk = None  # Set primary key to None to create a new object
        post.save()
duplicate_selected_posts.short_description = "Duplicate selected posts"

class TagSEOInline(admin.StackedInline):
    model = TagsSEO
    can_delete = False
class CatSEOInline(admin.StackedInline):
    model = CategorySEO
    can_delete = False
class SEOInline(admin.StackedInline):
    model = PostSEO
    can_delete = False

class PostAdmin(ImportExportModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    resource_class = PostResource
    date_hierarchy = 'create_date'
    list_display = ('image_tag','id','title' ,'create_date', 'slug', 'categories')
    list_filter = ('create_date', )
    search_fields = ['title', 'desc_1', 'desc_2', 'slug']
    inlines = [SEOInline]
    
    def display_category(self, obj):
        return ", ".join(tag.name for tag in obj.categories.all())
    display_category.short_description = 'categories'

admin.site.register(Post, PostAdmin)

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
class SliderModelAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
admin.site.register(SliderModel,SliderModelAdmin)

