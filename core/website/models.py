from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils.text import slugify
# Create your models here.

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
        return reverse('website:blog-category', kwargs={'slug': self.slug})

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
        return reverse('website:blog-tags', kwargs={'slug': self.slug})
    
class Post(models.Model):
    STATUS_CHOICES = ( 
        ('draft', 'Draft'), 
        ('published', 'Published'), 
    ) 

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length = 250, null = True, blank = True , unique=True)

    desc_1 = HTMLField(null = True, blank = True )
    desc_2 = HTMLField(null = True, blank = True )
    post_summery = HTMLField(null = True, blank = True )
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    tags = models.ManyToManyField (Tags)
    image = models.ImageField( upload_to= 'posts/thumbnails/%Y/%m' , default='posts/thumbnails/squre_images/1.jpg')
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(null=True)
    author = models.ForeignKey(User , on_delete=models.CASCADE, blank=True, null=True)
    total_views = models.IntegerField(default=0)
    blog_status = models.CharField(max_length=100 , choices=STATUS_CHOICES, default='Draft',blank = True, null = True)

    class Meta: 
        ordering = ('-publish_date', ) 
  
    def __str__(self): 
        return "{} - {} " .format(self.title, self.id) 
    
    def get_absolute_url(self):
        return reverse('website:blog-detail',
                        kwargs={'slug': self.slug})
    
class PostSEO(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='seo_images/', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post')
    def __str__(self):
        return self.title
    
class TagsSEO(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='seo_images/', null=True, blank=True)
    tags_seo = models.ForeignKey(Tags, on_delete=models.CASCADE, blank=True, null=True, related_name='posttags')
    def __str__(self):
        return self.title
    
class CategorySEO(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='seo_images/', null=True, blank=True)
    Category_seo = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='postcategory')
    def __str__(self):
        return self.title
        
class SliderModel(models.Model):
    title = models.CharField(max_length=255)
    alt = models.CharField(max_length=255)
    image = models.ImageField(upload_to='slider/', null=True, blank=True)
        
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'comment by {self.name} on {self.post}'