from django.http import HttpResponse
# slug is required
import string, random 
from django.utils.text import slugify 
# blog neede
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
# class base view
from django.views.generic.list import ListView
# models.fields
from website.models import SliderModel,CategorySEO, Post, Category , Tags ,PostSEO, TagsSEO
from product.models import Product ,PriceList

def index(request):
    posts = Post.objects.all().order_by('-id')
    products = Product.objects.all().order_by('-publish_date')
    categories = Category.objects.all()
    tags = Tags.objects.all()
    pricelist = PriceList.objects.filter().first()
    images = SliderModel.objects.all()

    context = {'posts': posts,
                'products':products,
                'categories':categories,         
                'tags':tags,
                'pricelist':pricelist,
                'images':images,
                }

    return render (request,'website/index.html', context)

def aboutus(request):
    return render (request,'website/about.html')

def contactus(request):
    return render (request,'website/contact.html')

def category(request):
    categories = Category.objects.filter(parent__isnull=True)  # top-level categories
    return render(request, 'website/blog.html', {'categories': categories})


def postcategory(request, slug):
    category = get_object_or_404(Category, slug=slug)  # Retrieve the category object based on the slug
    posts = Post.objects.filter(categories=category)  # Filter posts based on the category object

    seo = CategorySEO.objects.filter(Category_seo=category).first()

    paginator = Paginator(posts, 8)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    context = {'category': category, 'page_obj': page_obj, 'seo': seo, 'posts' : posts}

    return render(request, 'website/category.html', context)

def posttags(request, slug):
    tag = get_object_or_404(Tags, slug=slug)  # Retrieve the category object based on the slug
    posts = Post.objects.filter(tags=tag)  # Filter posts based on the category object
    seo = TagsSEO.objects.filter(tags_seo=tag).first()

    paginator = Paginator(posts, 8)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'tag': tag,'page_obj' :page_obj , 'posts': posts, 'seo' : seo}
    return render(request, 'website/tags.html', context)


def blog(request):
    posts = Post.objects.all().order_by('publish_date')
    products = Product.objects.all().order_by('publish_date')[:5]
    categories = Category.objects.all()
    tags = Tags.objects.all()


    paginator = Paginator(posts, 8)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    latests = Post.objects.all().order_by('publish_date')[:5]  # Example: fetching the 1 latest posts
    context = {'posts': posts,
                'latests': latests,
                'products':products,
                'categories':categories,         
                'tags':tags,
                'page_obj' :page_obj}
    return render(request, 'website/blog.html', context)

def blogposts(request, slug): 
    post = get_object_or_404(Post, slug =slug )
    seo = PostSEO.objects.filter(post=post).first()  # Retrieve the first PostSEO object associated with the post
    posts = Post.objects.all().order_by('-id')[:4]
    products = Product.objects.all().order_by('-id')[:4]
    categories = Category.objects.all()
    tags = Tags.objects.all()
    related_posts = Post.objects.filter()

    context = {'slug': slug,
               'post' : post,
               'seo' : seo,
               'posts': posts,
               'products':products,
               'categories':categories,
               'tags' : tags,
               'related_posts' : related_posts,
               }

    return render(request, 'website/blog-detail.html', context) 


def ProductShop(request):
    pricelist = PriceList.objects.filter().first()
    products = Product.objects.all().order_by('publish_date')[1:]
    latests = Post.objects.all().order_by('publish_date')[:1]  # Example: fetching the 1 latest posts

    paginator = Paginator(products, 8)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products,
                'latests': latests,
                'pricelist':pricelist,
                'page_obj':page_obj
                }

    return render (request,'website/shop.html', context)
def TermsAndCondition(request):
    return render (request , 'website/termandcondition.html')
def test(request):

    categories = Category.objects.all()

    context = {'categories': categories,}
    return render (request , 'test.html', context)

def comingsoon (request):
    return render (request , 'website/comming-soon.html')


def page404 (request):
    return render (request , 'website/404.html')

class SoilListView (ListView):
    model = Product
    template_name = "productcat/soil.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 10  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='az1').order_by('publish_date')
    
class ConcreteListView (ListView):
    model = Product
    template_name = "productcat/concrete.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 10  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='az2').order_by('publish_date')
    
class AsphaltListView (ListView):
    model = Product
    template_name = "productcat/asphalt.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 10  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='az3').order_by('publish_date')
    
    
class RockListView (ListView):
    model = Product
    template_name = "productcat/rock.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 10  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='az4').order_by('publish_date')
    
                        
class WeldListView (ListView):
    model = Product
    template_name = "productcat/weld.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 10  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='az7').order_by('publish_date')
                        

