from django.http import HttpResponse, HttpResponseNotFound
# slug is required
import string, random 
from django.utils.text import slugify 
# blog neede
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
# class base view
from django.views.generic.list import ListView
# models.fields
from website.models import SliderModel,CategorySEO, Post, Category , Tags ,PostSEO, TagsSEO, PopupAlert
from product.models import Product ,PriceList
# forms.fields
from .forms import EmailPostForm, CommentForm, SearchForm   
# search fields
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate
from django.http import JsonResponse
#review model
from review.models import PostReviewModel, ReviewStatusType
def handler_404(request, exception=None, template_name="errors/404.html"):
    context = {}  # You can pass context variables to the template if needed
    return render(request, template_name, context, status=404)
def handler_500(request, exception=None, template_name="errors/500.html"):
    context = {}  # You can pass context variables to the template if needed
    return render(request, template_name, context, status=500)
def handler_403(request, exception=None, template_name="errors/403.html"):
    context = {}  # You can pass context variables to the template if needed
    return render(request, template_name, context, status=403)
def handler_400(request, exception=None, template_name="errors/400.html"):
    context = {}  # You can pass context variables to the template if needed
    return render(request, template_name, context, status=400)

def set_language(request):
    lang_code = request.GET.get('language')
    print("Selected Language Code:", lang_code)  # Debug print
    if lang_code:
        activate(lang_code)
        request.session['django_language'] = lang_code  # Store language in session
        return JsonResponse({'status': 'success', 'language': lang_code})
    
    return JsonResponse({'status': 'error', 'message': 'Language not provided'})

def index(request):
    # Check if the language is not already set in session
    if 'django_language' not in request.session:
        activate('fa')  # Set default language to Farsi
        request.session['django_language'] = 'fa'  # Store language in session
    posts = Post.objects.all().order_by('-id')[:5]
    products = Product.objects.all().order_by('-publish_date')[:5]
    categories = Category.objects.all()
    tags = Tags.objects.all()
    pricelist = PriceList.objects.filter().first()
    images = SliderModel.objects.all()
    popupalert = PopupAlert.objects.first()

    context = {'posts': posts,
                'products':products,
                'categories':categories,         
                'tags':tags,
                'pricelist':pricelist,
                'images':images,
                'popupalert':popupalert,
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
    post = get_object_or_404(Post, slug=slug )

    # --- 1) Handle POST request (submitting a new review) ---
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        rate = request.POST.get('rate', 5)  # default to 5 if not provided

        # You can validate input as needed before creating the review.
        # Setting status to 'pending' by default (or immediately 'accepted' 
        # if no moderation is needed).
        PostReviewModel.objects.create(
            name=name,
            email=email,
            description=description,
            rate=rate,
            post=post,
            status=ReviewStatusType.pending.value  # or .accepted.value
        )
        # Redirect to the same page so the user sees their review (or a success message).
        return redirect('website:blog-detail', slug=slug)

    # --- 2) Retrieve existing accepted reviews ---
    reviews = PostReviewModel.objects.filter(
        post=post,
        status=ReviewStatusType.accepted.value
    )
    total_reviews_count = reviews.count()

    # Calculate distribution count for each rate
    reviews_count = {
        f"rate_{rate}": reviews.filter(rate=rate).count() 
        for rate in range(1, 6)
    }

    # Calculate distribution percentage for each rate
    if total_reviews_count > 0:
        reviews_avg = {
            f"rate_{rate}": round(
                (reviews.filter(rate=rate).count() / total_reviews_count) * 100, 2
            )
            for rate in range(1, 6)
        }
    else:
        reviews_avg = {f"rate_{rate}": 0 for rate in range(1, 6)}

    # --- 3) Prepare your context ---
    # You mentioned you have other objects: posts, products, categories, tags...
    posts = Post.objects.all().order_by('-id')[:4]
    products = Product.objects.all().order_by('-id')[:4]  # if relevant
    categories = Category.objects.all()
    tags = Tags.objects.all()
    related_posts = Post.objects.filter()  # Adjust query as needed
    seo = PostSEO.objects.filter(post=post).first()

    context = {
        'slug': slug,
        'post': post,
        'seo': seo,
        'posts': posts,
        'products': products,
        'categories': categories,
        'tags': tags,
        'related_posts': related_posts,

        'reviews': reviews,
        'total_reviews_count': total_reviews_count,
        'reviews_count': reviews_count,
        'reviews_avg': reviews_avg
    }

    return render(request, 'website/blog-detail.html', context)

def ProductShop(request):
    products = Product.objects.all().order_by('publish_date')[1:]
    latests = Post.objects.all().order_by('publish_date')[:1]  # Example: fetching the 1 latest posts

    paginator = Paginator(products, 12)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products,
                'latests': latests,
                'page_obj':page_obj,
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

def offerland(request):
    pricelist = PriceList.objects.filter().first()
    context = {'pricelist': pricelist,}

    return render (request , 'website/offer-landing.html' , context)

def page404 (request):
    return render (request , 'website/404.html')

class SoilListView (ListView):
    model = Product
    template_name = "productcat/soil.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 12  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='soil-equipments').order_by('publish_date')
    
class ConcreteListView (ListView):
    model = Product
    template_name = "productcat/concrete.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 12  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='concrete-equipments').order_by('publish_date')
    
class AsphaltListView (ListView):
    model = Product
    template_name = "productcat/asphalt.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 12  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='asphalt-equipments').order_by('publish_date')
     
class RockListView (ListView):
    model = Product
    template_name = "productcat/rock.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 12  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='rock-equipments').order_by('publish_date')
                         
class WeldListView (ListView):
    model = Product
    template_name = "productcat/weld.html" 
    context_object_name = 'products' 
    ordering = ['-publish_date'] 
    paginate_by = 12  # Display 10 products per page

    def get_queryset(self):
        return Product.objects.filter(categories__name='weld-equipments').order_by('publish_date')
                        
# search view
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            # A B C D => 1.0 , 0.4 , 0.2 , 0.1
            search_vector = SearchVector('title', weight='A') + \
                SearchVector('body', weight="C")
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector, rank=SearchRank(
                search_vector, search_query)).filter(rank__gte=0.5).order_by('-rank')
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})

