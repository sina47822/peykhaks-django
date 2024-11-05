"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from website.sitemaps import StaticViewSitemap,BlogSitemap,BlogTagSitemap,BlogCategorySitemap
from product.sitemaps import ProductTagsSitemap,ProductCategorySitemap,ProductSitemap
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.i18n import set_language

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'blogcategory': BlogCategorySitemap,
    'blogtags': BlogTagSitemap,
    'product': ProductSitemap,
    'productcategory': ProductCategorySitemap,
    'producttags': ProductTagsSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tarjome/', include('rosetta.urls')),

    path('product/', include('product.urls')),
    path('review/', include('review.urls')),

    path('', include('website.urls')),
    path('tinymce/', include('tinymce.urls')),
    
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
] 

# Custom error handlers
handler400 = 'website.views.handler_400'
handler403 = 'website.views.handler_403'
handler404 = 'website.views.handler_404'
handler500 = 'website.views.handler_500'
# serving static and media for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)