from django.shortcuts import get_object_or_404, render
from product.models import Product , Category, Tags ,PriceList,ProductSEO,TagsSEO,CategorySEO
from .forms import PriceUpdateFormset
from django.core.paginator import Paginator

from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from product.forms import ProductForm

def productcategory(request, slug):
    category = get_object_or_404(Category, slug=slug)  # Retrieve the category object based on the slug
    products = Product.objects.filter(categories=category)  # Filter posts based on the category object
    seo = CategorySEO.objects.filter(Category_seo=category).first()
    context = {'slug': slug,
               'category': category,
                'products': products,
                'seo' : seo}
    return render(request, 'product/category.html', context)

def producttags(request, slug):
    tags = get_object_or_404(Tags, slug=slug)  
    products = Product.objects.filter(tags=tags)  
    seo = TagsSEO.objects.filter(tags_seo=tags).first()

    context = {'slug': slug,
               'tags': tags,
               'products': products,
               'seo' : seo}
    return render(request, 'product/tags.html', context)

def products_detail(request, slug): 

    product = get_object_or_404(Product, slug =slug )
    seo = ProductSEO.objects.filter(product=product).first()  # Retrieve the first PostSEO object associated with the post
    # Retrieve tags and category related to the product
    tags = product.tags.all()
    category = product.categories

    context = {'slug': slug,
               'product' : product,
                'seo' : seo,
                'tags': tags,
                'category': category,
               }

    return render(request, 'product/product-detail.html', context) 

def price_list(request):
    pricelist = PriceList.objects.filter().first()
    templates = 'partials/price-list.html'
    context = {'pricelist':pricelist}

    return render (request , templates, context)


class ProductList(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    # paginate_by = 10
    ordering = 'id'
class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
class ProductCreateView(CreateView):
    model = Product
    fields = ['id','title','Code', 'price', 'offer_price','stock','description','summery','categories','tags','publish_date','author','is_active','guarantee','time_to_bring','size','standard']
    template_name = 'product/product_form.html'
    success_url = '/product/'

    def form_valid(self, form):
        return super().form_valid(form)
class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    success_url = '/product/'

class ProductDeleteView(LoginRequiredMixin,DeleteView):
    model = Product
    success_url = '/product/'