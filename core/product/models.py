from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils.text import slugify


    
class StandardASTM(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    value = models.FileField(upload_to='standards/ASTM/', null=True, blank=True)
    def __str__(self):
        return self.name if self.name else "No Name"
    
class StandardAASHTO(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    value = models.FileField(upload_to='standards/AASHTO/', null=True, blank=True)
    def __str__(self):
        return self.name if self.name else "No Name"
    
class StandardISIRI(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    value = models.FileField(upload_to='standards/ISIRI/', null=True, blank=True)
    def __str__(self):
        return self.name if self.name else "No Name"

class Standards(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True, null=True,unique=True)
    standard_astm=models.ForeignKey(StandardASTM, on_delete=models.CASCADE,blank=True, null=True)
    standard_aashto =models.ForeignKey(StandardAASHTO, on_delete=models.CASCADE,blank=True, null=True)
    standard_isiri =models.ForeignKey(StandardISIRI, on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.title
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
        
    def __str__(self):
        return self.title

class Category(models.Model):
    name= models.CharField(max_length=200)
    slug = models.SlugField(max_length = 250, null = True, blank = True , unique=True)
    parent = models.ForeignKey('self' , on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)  # ensures unique slugs in the same parent category
        
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
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length = 250, null = True, blank = True , unique=True)
    Code = models.CharField(max_length=15, null = True, unique=True)
    description = HTMLField(null = True, blank = True )
    summery = HTMLField(null = True, blank = True )
    price = models.DecimalField(max_digits=10, decimal_places=0)
    offer_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    image = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)

    category = models.ManyToManyField(ProductCategoryModel) #add at the other time
    status = models.IntegerField(choices=ProductStatusType.choices,default=ProductStatusType.draft.value)

    categories = models.ForeignKey(Category, on_delete=models.SET_NULL ,related_name='products', blank=True, null=True)
    tags = models.ManyToManyField (Tags)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(null=True)
    author = models.ForeignKey(User , on_delete=models.CASCADE, blank=True, null=True)
    total_views = models.IntegerField(default=0 , )
    is_active = models.CharField(max_length=100 , choices=STATUS_CHOICES, default='not_active',blank = True, null = True)

    stock = models.PositiveIntegerField(blank = True, null = True,)
    standard = models.ManyToManyField (Standards)
    size = models.CharField(max_length=255 , choices=SIZE_CHOICES,default='Medium')
    guarantee = models.BooleanField(default=True)
    time_to_bring = models.CharField(max_length=255,blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product:productdetails', kwargs={'slug': self.slug})

class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    media_file = models.FileField(upload_to='product_media/%Y/%m')

    def __str__(self):
        return f"{self.product.title} - {self.media_type}"

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.title} - {self.name}: {self.value}"
    
class ProductSEO(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='seo_images/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='product')
    def __str__(self):
        return self.title
    
class TagsSEO(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='seo_images/', null=True, blank=True)
    tags_seo = models.ForeignKey(Tags, on_delete=models.CASCADE, blank=True, null=True, related_name='tags')
    def __str__(self):
        return self.title
    
class CategorySEO(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='seo_images/', null=True, blank=True)
    Category_seo = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    def __str__(self):
        return self.title
    
class PriceList(models.Model):
    title = models.CharField(max_length=120, null=True, blank=True)
    upload_date = models.TextField(null=True, blank=True)
    beton_1_document = models.FileField(upload_to='doc/beton1/', null=True, blank=True)
    beton_2_document = models.FileField(upload_to='doc/beton2/', null=True, blank=True)
    beton_3_document = models.FileField(upload_to='doc/beton3/', null=True, blank=True)
    khak_1_document = models.FileField(upload_to='doc/khak1/', null=True, blank=True)
    khak_2_document = models.FileField(upload_to='doc/khak2/', null=True, blank=True)
    khak_3_document = models.FileField(upload_to='doc/khak3/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class WishlistProductModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.title