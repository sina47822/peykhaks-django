from django.urls import path
from website.views import aboutus,contactus,index,blog,blogposts,ProductShop,TermsAndCondition, test, postcategory,posttags
from product.views import price_list
app_name = 'website'

urlpatterns = [
    path('', index , name='home'),
    path('about-us/', aboutus, name='about'),
    path('contact-us/', contactus, name='contact'),
    path('blog/', blog , name='blog-list'),
    path('shop/', ProductShop, name='shop'),
    path('terms-and-conditions/', TermsAndCondition, name='Terms-and-conditions'),

        
    path('blog/geotechnics/', blogposts, name='soil-laboratory'),
    path('blog/concrete/', blogposts, name='concrete-laboratory'),
    path('blog/asphalt/', blogposts, name='asphalt-laboratory'),
    path('blog/rock/', blogposts, name='rock-laboratory'),
    path('blog/general/', blogposts, name='general-laboratory'),

    path('test/', test, name='test'),
    path('category/<slug:slug>/',postcategory , name='blog-category'),
    path('tags/<slug:slug>/',posttags , name='blog-tags'),

    path('<slug:slug>/',blogposts , name='blog-detail'),

]