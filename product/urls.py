from django.urls import path
from product.views import products_detail, product_list, producttags, productcategory, price_list

app_name = 'product'

urlpatterns = [
    path('category/<slug:slug>/', productcategory, name='productcategory'),
    path('tags/<slug:slug>/', producttags, name='producttags'),
    path('pricelists/', price_list, name='pricelists'),
    path('<slug:slug>/', products_detail, name='productdetails'),
]