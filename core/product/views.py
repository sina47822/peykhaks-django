from django.shortcuts import get_object_or_404, render
from product.models import Product , Category, Tags ,PriceList,ProductSEO,TagsSEO,CategorySEO
from .forms import PriceUpdateFormset
from django.core.paginator import Paginator

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

def product_list(request):
    products = Product.objects.all()
    
    if request.method == 'POST':
        formset = PriceUpdateFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
    else:
        formset = PriceUpdateFormset(queryset=products)

    context = {
        'products': products,
        'formset': formset,
        'page_obj':page_obj
    }
    return render(request, 'product/product_list.html', context)

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


