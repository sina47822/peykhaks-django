from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


    
class StandardASTM(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    value = models.FileField(upload_to='standards/ASTM/', null=True, blank=True)
    def __str__(self):
        return self.name if self.name else "No Name"
    class Meta:
        verbose_name = _('استاندارد ASTM')
        verbose_name_plural = verbose_name

class StandardAASHTO(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    value = models.FileField(upload_to='standards/AASHTO/', null=True, blank=True)
    def __str__(self):
        return self.name if self.name else "No Name"
    class Meta:
        verbose_name = _('استاندارد آشو')
        verbose_name_plural = verbose_name
    
class StandardISIRI(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    value = models.FileField(upload_to='standards/ISIRI/', null=True, blank=True)
    def __str__(self):
        return self.name if self.name else "No Name"
    class Meta:
        verbose_name = _('استاندارد ایران')
        verbose_name_plural = verbose_name

class Standards(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True, null=True,unique=True)
    standard_astm=models.ForeignKey(StandardASTM, on_delete=models.CASCADE,blank=True, null=True)
    standard_aashto =models.ForeignKey(StandardAASHTO, on_delete=models.CASCADE,blank=True, null=True)
    standard_isiri =models.ForeignKey(StandardISIRI, on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('استانداردها')
        verbose_name_plural = verbose_name

class ProductStatusType(models.IntegerChoices):
    publish = 1 ,("نمایش")
    draft = 2 ,("عدم نمایش")

class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_date"]
        verbose_name = _('دسته بندی محصولات')
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.title

class Category(models.Model):
    name= models.CharField(max_length=200)
    slug = models.SlugField(max_length = 250, null = True, blank = True , unique=True)
    parent = models.ForeignKey('self' , on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)  # ensures unique slugs in the same parent category
        verbose_name = _('دسته بندی محصولات')
        verbose_name_plural = verbose_name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product:productcategory', kwargs={'slug': self.slug})

class Tags(models.Model):
    name= models.CharField(max_length=200)
    slug = models.SlugField(max_length = 250, null = True, blank = True , unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:producttags', kwargs={'slug': self.slug})
    class Meta:
        verbose_name = _('تگ ها')
        verbose_name_plural = verbose_name

class Product(models.Model):

    STATUS_CHOICES = ( 
        ('active', 'active'), 
        ('not_active', 'not_active'), 
    ) 
    SIZE_CHOICES = ( 
        ('light', 'light'), 
        ('Heavy', 'Heavy'), 
        ('Medium', 'Medium'), 

    ) 
    title = models.CharField(_('عنوان محصول'),max_length=255)
    slug = models.SlugField(_('اسلاگ محصول'),max_length = 250, null = True, blank = True , unique=True)
    Code = models.CharField(_('کد محصول'),max_length=15, null = True, unique=True)
    description = HTMLField(_('متن محصول'),null = True, blank = True )
    summery = HTMLField(_('خلاصه متن'),null = True, blank = True )
    price = models.DecimalField(_('قیمت محصول'),max_digits=10, decimal_places=0)
    offer_price = models.DecimalField(_('قیمت با تخفیف'),max_digits=10, decimal_places=0, blank=True, null=True)
    image = models.ImageField(_('تصویر عکس'),upload_to='products/thumbnails/', blank=True, null=True)

    category = models.ManyToManyField(ProductCategoryModel) #add at the other time
    status = models.IntegerField(_('وضعیت محصول'),choices=ProductStatusType.choices,default=ProductStatusType.draft.value)

    avg_rate = models.FloatField(_('نمره محصول'),default=0.0)

    categories = models.ForeignKey(Category, on_delete=models.SET_NULL ,related_name='products', blank=True, null=True)
    tags = models.ManyToManyField (Tags)
    update_date = models.DateTimeField(_('زمان به روز رسانی'),auto_now=True)
    create_date = models.DateTimeField(_('زمان تولید'),auto_now_add=True)
    publish_date = models.DateTimeField(_('زمان انتشار'),null=True)
    author = models.ForeignKey(User ,on_delete=models.CASCADE, blank=True, null=True)
    total_views = models.IntegerField(_('مجموع بازدید'),default='14' , blank=True, null=True )
    is_active = models.CharField(_('فعال بودن'),max_length=100 , choices=STATUS_CHOICES, default='not_active',blank = True, null = True)

    stock = models.PositiveIntegerField(_('تعداد'),blank = True, null = True,)
    standard = models.ManyToManyField (Standards,_('استاندارد'))
    size = models.CharField(_('اندازه'),max_length=255 , choices=SIZE_CHOICES,default='Medium')
    guarantee = models.BooleanField(_('گارانتی'),default=True)
    time_to_bring = models.CharField(_('زمان ارسال'),max_length=255,blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product:productdetails', kwargs={'slug': self.slug})
    class Meta:
        verbose_name = _('محصولات')
        verbose_name_plural = verbose_name

class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(_('نوع رسانه'),max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    media_file = models.FileField(_('فایل مدیا'),upload_to='product_media/%Y/%m')

    def __str__(self):
        return f"{self.product.title} - {self.media_type}"
    class Meta:
        verbose_name = _('تصاویر محصولات')
        verbose_name_plural = verbose_name

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(_('نام مشخصه محصول'),max_length=255)
    value = models.CharField(_('مقدار مشخصه محصول'),max_length=255)
    class Meta:
        verbose_name = _('مشخصات محصولات')
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.product.title} - {self.name}: {self.value}"
    
class ProductSEO(models.Model):
    title = models.CharField(_('عنوان سئو محصول'),max_length=255)
    description = models.TextField(_('توضیحات سئو محصول'),)
    image = models.ImageField(_('عکس سئو محصول'),upload_to='seo_images/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='product')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _('سئو محصولات')
        verbose_name_plural = verbose_name

class TagsSEO(models.Model):
    title = models.CharField(_('عنوان سئو تگ'),max_length=255)
    description = models.TextField(_('توضیحات سئو تگ'),)
    image = models.ImageField(_('تصویر سئو تگ'),upload_to='seo_images/', null=True, blank=True)
    tags_seo = models.ForeignKey(Tags, on_delete=models.CASCADE, blank=True, null=True, related_name='tags')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _('سئو تگ')
        verbose_name_plural = verbose_name

class CategorySEO(models.Model):
    title = models.CharField(_('عنوان سئو دسته بندی'),max_length=255)
    description = models.TextField(_('توضیحات سئو دسته بندی'),)
    image = models.ImageField(_('تصویر سئو دسته بندی'),upload_to='seo_images/', null=True, blank=True)
    Category_seo = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _('سئو دسته بندی')
        verbose_name_plural = verbose_name

class PriceList(models.Model):
    title = models.CharField(_('عنوان لیست قیمت'),max_length=120, null=True, blank=True)
    upload_date = models.TextField(_('تاریخ به روز رسانی لیست قیمت'),null=True, blank=True)
    beton_1_document = models.FileField(_('فایل بتن پایه یک'),upload_to='doc/beton1/', null=True, blank=True)
    beton_2_document = models.FileField(_('فایل بتن پایه دو'),upload_to='doc/beton2/', null=True, blank=True)
    beton_3_document = models.FileField(_('فایل بتن پایه سه'),upload_to='doc/beton3/', null=True, blank=True)
    khak_1_document = models.FileField(_('فایل خاک پایه یک'),upload_to='doc/khak1/', null=True, blank=True)
    khak_2_document = models.FileField(_('فایل خاک پایه دو'),upload_to='doc/khak2/', null=True, blank=True)
    khak_3_document = models.FileField(_('فایل خاک پایه سه'),upload_to='doc/khak3/', null=True, blank=True)
    class Meta:
        verbose_name = _('لیست قیمت محصولات')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
    
class WishlistProductModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    class Meta:
        verbose_name = _('محصولات مورد علاقه')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product.title

class PageConfig(models.Model):
    page_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # Add slug field
    logo = models.ImageField(upload_to='logos/')
    last_update = models.CharField(max_length=255)
    last_changes = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.page_name)  # Automatically generate slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.page_name
    
class PageConfigProduct(models.Model):
    page_config = models.ForeignKey('PageConfig', on_delete=models.CASCADE, related_name='page_config_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # تعداد محصول

    def __str__(self):
        return f'{self.product.title} - {self.quantity}'