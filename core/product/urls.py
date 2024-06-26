from django.urls import path
from . import views
app_name = 'product'

urlpatterns = [
    path('category/<slug:slug>/', views.productcategory, name='productcategory'),
    path('tags/<slug:slug>/', views.producttags, name='producttags'),
    path('pricelists/', views.price_list, name='pricelists'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<slug:slug>/edit/', views.ProductUpdateView.as_view(), name='product-edit'),
    path('<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('', views.ProductList.as_view(), name='product-list'),
    path('p/<slug:slug>/', views.ProductDetail.as_view(), name='product-detail'),
    path('<slug:slug>/', views.products_detail, name='productdetails'),
]