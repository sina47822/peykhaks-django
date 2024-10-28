from django.urls import path
from website.views import aboutus,contactus,index,blog,blogposts,ProductShop,TermsAndCondition, test, postcategory,posttags,comingsoon,page404,offerland,post_search, SoilListView,WeldListView,RockListView,AsphaltListView,ConcreteListView
from product.views import price_list
from django.utils.translation import gettext_lazy as _

app_name = 'website'

urlpatterns = [
    path('', index , name='home'),
    path('about-us/', aboutus, name='about'),
    path('404/', page404 , name='404'),
    path('coming-soon/', comingsoon, name='coming-soon'),
    path('offer-landing/', offerland, name='offer-landing'),
    path('search/',post_search,name="post_search"),

    path('contact-us/', contactus, name='contact'),
    path('blog/', blog , name='blog-list'),
    path('shop/', ProductShop, name='shop'),
    path('terms-and-conditions/', TermsAndCondition, name='Terms-and-conditions'),

        
    path('geotechnics/', SoilListView.as_view(), name='soil-laboratory'),
    path('concrete/', ConcreteListView.as_view(), name='concrete-laboratory'),
    path('asphalt/', AsphaltListView.as_view(), name='asphalt-laboratory'),
    path('rock/', RockListView.as_view(), name='rock-laboratory'),
    path('weld/', WeldListView.as_view(), name='weld-laboratory'),

    path('test/', test, name='test'),
    path('category/<slug:slug>/',postcategory , name='blog-category'),
    path('tags/<slug:slug>/',posttags , name='blog-tags'),

    path('<slug:slug>/',blogposts , name='blog-detail'),

]