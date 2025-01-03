from django.contrib import sitemaps
from django.urls import reverse

from django.contrib.sitemaps import Sitemap
from website.models import Post, Category, Tags

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "weekly"
    
    def items(self):
        return ['website:home','website:about','website:contact','website:blog-list','website:shop','website:Terms-and-conditions','website:weld-laboratory','website:rock-laboratory','website:asphalt-laboratory','website:concrete-laboratory','website:soil-laboratory','website:offer-landing']
        
    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return obj.get_absolute_url()
        
class BlogCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.all()
        
    def location(self, obj):
        return obj.get_absolute_url()

class BlogTagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Tags.objects.all()
        
    def location(self, obj):
        return obj.get_absolute_url()
