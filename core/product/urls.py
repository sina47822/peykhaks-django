from django.urls import path,re_path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'product'

urlpatterns = [


    path('category/<slug:slug>/', views.productcategory, name='productcategory'),
    path('tags/<slug:slug>/', views.producttags, name='producttags'),
    path('pricelists/', views.price_list, name='pricelists'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<slug:slug>/edit/', views.ProductUpdateView.as_view(), name='product-edit'),
    path('<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('', views.ProductList.as_view(), name='product-list'),
    path("grid/",views.ShopProductGridView.as_view(),name="product-grid"),
    path("add-or-remove-wishlist/",views.AddOrRemoveWishlistView.as_view(),name="add-or-remove-wishlist"),

    # path('p/<slug:slug>/', views.ProductDetail.as_view(), name='product-detail'),
    path('<slug:slug>/' ,views.ShopProductDetailView.as_view(),name="productdetails"),

    re_path( r"(?P<slug>[-\w]+)",views.ShopProductDetailView.as_view(),name="productdetails"),

    # path('<slug:slug>/', views.products_detail, name='productdetails'),

]