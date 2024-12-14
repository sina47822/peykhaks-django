from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from website.models import Post, Category, SliderModel, Tags, PostSEO,TagsSEO,CategorySEO,PopupAlert
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils.html import format_html
from website.utils import export_posts_to_excel, import_posts_from_excel

class ImportExcelForm(forms.Form):
    excel_file = forms.FileField()

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

# class PostAdmin(ImportExportModelAdmin):
#     def image_tag(self, obj):
#         return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

#     resource_class = PostResource
#     date_hierarchy = 'create_date'
#     list_display = ('image_tag','id','title' ,'create_date', 'slug', 'categories')
#     list_filter = ('create_date', )
#     search_fields = ['title', 'desc_1', 'desc_2', 'slug']
#     inlines = [SEOInline]
    
#     def display_category(self, obj):
#         return ", ".join(tag.name for tag in obj.categories.all())
#     display_category.short_description = 'categories'
class PostAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
    date_hierarchy = 'create_date'
    list_display = ('image_tag','id','title' ,'create_date', 'slug', 'categories')
    list_filter = ('create_date', )
    search_fields = ['title', 'desc_1', 'desc_2', 'slug']
    inlines = [SEOInline]
    
    def display_category(self, obj):
        return ", ".join(tag.name for tag in obj.categories.all())
    display_category.short_description = 'categories'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.import_excel, name='post_import_excel'),
            path('export-excel/', self.export_excel, name='post_export_excel'),
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
                import_posts_from_excel(form.cleaned_data['excel_file'])
                self.message_user(request, "Posts imported successfully!")
                return redirect("..")
        else:
            form = ImportExcelForm()
        return render(request, "admin/import_excel.html", {"form": form})

    def export_excel(self, request):
        return export_posts_to_excel()
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

class PopupAlertAdmin(admin.ModelAdmin):
    list_display = ('alert_title', 'alert_control', 'popup_title', 'popup_control')
    list_editable = ('alert_control', 'popup_control')  # Allow toggling directly in the admin list
    fields = ('alert_title', 'alert_control', 'popup_title', 'popup_image', 'popup_control')

admin.site.register(PopupAlert, PopupAlertAdmin)