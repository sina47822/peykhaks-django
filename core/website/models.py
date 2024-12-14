from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils.text import slugify
# Create your models here.
from django.utils.translation import gettext_lazy as _

# advertise-landscape-1
# advertise-landscape-2
# categories
# tags
# last-modifide
# publish-date
# author
# views
# total-comments
    
class Category(models.Model):
    name= models.CharField(_('نام دسته بندی'),max_length=200)
    slug = models.SlugField(_('اسلاگ دسته بندی'),max_length = 250, null = True, blank = True , unique=True)
    parent = models.ForeignKey('self' , on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)  # ensures unique slugs in the same parent category
        verbose_name = _('دسته بندی مقالات')
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('website:blog-category', kwargs={'slug': self.slug})

class Tags(models.Model):
    name= models.CharField(_('عنوان تگ'),max_length=200)
    slug = models.SlugField(_('اسلاگ تگ'),max_length = 250, null = True, blank = True , unique=True)
    
    class Meta:
        verbose_name = _('تگ ها')
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('website:blog-tags', kwargs={'slug': self.slug})
    
class Post(models.Model):
    STATUS_CHOICES = ( 
        ('draft', 'Draft'), 
        ('published', 'Published'), 
    ) 

    title = models.CharField(_('عنوان'),max_length=255)
    slug = models.SlugField(_('اسلاگ'),max_length = 250, null = True, blank = True , unique=True)

    desc_1 = HTMLField(_('متن اول'),null = True, blank = True )
    desc_2 = HTMLField(_('متن دوم'),null = True, blank = True )
    post_summery = HTMLField(_('خلاصه مقاله'),null = True, blank = True )
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    tags = models.ManyToManyField (Tags)
    image = models.ImageField(_('تصویر اصلی'), upload_to= 'posts/thumbnails/%Y/%m' , default='posts/thumbnails/squre_images/1.jpg')
    update_date = models.DateTimeField(_('تاریخ آپدیت'),auto_now=True)
    create_date = models.DateTimeField(_('تاریخ ساخت '),auto_now_add=True)
    publish_date = models.DateTimeField(_('زمان انتشار'),null=True)
    author = models.ForeignKey(User , on_delete=models.CASCADE, blank=True, null=True)
    total_views = models.IntegerField(_('تعداد بازدید'),default=0)
    blog_status = models.CharField(_('وضعیت انتشار'),max_length=100 , choices=STATUS_CHOICES, default='Draft',blank = True, null = True)

    class Meta: 
        ordering = ('-publish_date', ) 
        verbose_name = _('مقالات')
        verbose_name_plural = verbose_name

    def __str__(self): 
        return "{} - {} " .format(self.title, self.id) 
    
    def get_absolute_url(self):
        return reverse('website:blog-detail',
                        kwargs={'slug': self.slug})
    
class PostSEO(models.Model):
    title = models.CharField(_('عنوان سئو'),max_length=50)
    description = models.TextField(_('توضیحات سئو'),max_length=200)
    image = models.ImageField(_('تصویر سئو'),upload_to='seo_images/', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _('سئو مقالات')
        verbose_name_plural = verbose_name

class TagsSEO(models.Model):
    title = models.CharField(_('عنوان سئو'),max_length=255)
    description = models.TextField(_('توضیحات سئو'),)
    image = models.ImageField(_('تصویر سئو'),upload_to='seo_images/', null=True, blank=True)
    tags_seo = models.ForeignKey(Tags, on_delete=models.CASCADE, blank=True, null=True, related_name='posttags')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _('سئو تگ ها')
        verbose_name_plural = verbose_name

class CategorySEO(models.Model):
    title = models.CharField(_('عنوان سئو'),max_length=255)
    description = models.TextField(_('توضیحات سئو'),)
    image = models.ImageField(_('تصویر سئو'),upload_to='seo_images/', null=True, blank=True)
    Category_seo = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='postcategory')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _('سئو دسته بندی ها')
        verbose_name_plural = verbose_name

class SliderModel(models.Model):
    title = models.CharField(_('نام تصویر'),max_length=255)
    alt = models.CharField(_('متن جایگزین'),max_length=255)
    image = models.ImageField(upload_to='slider/', null=True, blank=True)
        
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_('نام و نام خانوادگی'),max_length=50)
    email = models.EmailField(_('ایمیل'),max_length=254, null=True, blank=True)
    body = models.TextField(_('متن پیام'),)
    created = models.DateTimeField(_('تاریخ ساخت'),auto_now=False, auto_now_add=True)
    updated = models.DateField(_('تاریخ به روزرسانی'),auto_now=True)
    active = models.BooleanField(_(' فعال'),default=True)
    class Meta:
        verbose_name = _('کامنت ها')
        verbose_name_plural = verbose_name

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'comment by {self.name} on {self.post}'

class PopupAlert(models.Model):
    title = models.CharField(_('عنوان'),max_length=255,null=True,blank=True)
    alert_title = models.TextField(_('عنوان آلرت'),null=True,blank=True)
    alert_control = models.BooleanField(_('نمایش آلرت'), default=False)
    popup_title = models.TextField(_('عنوان پاپ آپ'),null=True,blank=True)
    popup_image = models.ImageField(
        _('تصویر پاپ آپ'),
        upload_to='popup_images/',
        null=True,
        blank=True
    )
    popup_control = models.BooleanField(_('نمایش پاپ آپ'), default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('پاپ آپ و آلرت')
        verbose_name_plural = verbose_name
