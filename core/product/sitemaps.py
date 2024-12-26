from django.contrib import sitemaps
from django.urls import reverse

from django.contrib.sitemaps import Sitemap
from product.models import Category, Tags, Product,PageConfig


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.update_date           

    def location(self, obj):
        return obj.get_absolute_url()
        
class ProductCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.all()
        
    def location(self, obj):
        return obj.get_absolute_url()

class ProductTagsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Tags.objects.all()
        
    def location(self, obj):
        return obj.get_absolute_url()

class ProductPricelistSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.4

    def items(self):
        return PageConfig.objects.all()
        
    def location(self, obj):
        return obj.get_absolute_url()