from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from review.models import ProductReviewModel, ReviewStatusType
from product.models import Product , Category, Tags ,PriceList,ProductSEO,TagsSEO,CategorySEO,ProductStatusType,ProductCategoryModel,WishlistProductModel,ProductSpecification,PageConfig
from .forms import PriceUpdateFormset
from django.core.paginator import Paginator

from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from product.forms import ProductForm
# from review.models import ReviewModel,ReviewStatusType

from django.core.exceptions import FieldError
from django.core.exceptions import PermissionDenied
# from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

#generate pdf
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

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
    specifications = product.specifications.all()
    other_photo = product.media.all()
    
    context = {'slug': slug,
               'product' : product,
                'seo' : seo,
                'tags': tags,
                'category': category,
                'specifications': specifications,
                'other_photo' : other_photo,
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

# class ProductDetail(DetailView):
#     model = Product
#     template_name = 'product/product-details.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Get the product's specifications
#         context['specifications'] = self.object.specifications.all()  # 'specifications' is the related_name in ProductSpecification
#         context['categories'] = self.object.categories
#         context['tags'] = self.object.tags.all()
#         return context
    
class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['id','title','Code', 'price', 'offer_price','stock','description','summery','categories','tags','publish_date','author','is_active','guarantee','time_to_bring','size','standard']
    template_name = 'product/product_form.html'
    success_url = '/product/'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied  # Raises a 403 error
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        return super().form_valid(form)
    
class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    success_url = '/product/'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied  # Raises a 403 error
        return super().dispatch(request, *args, **kwargs)

class ProductDeleteView(LoginRequiredMixin,DeleteView):
    model = Product
    success_url = '/product/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied  # Raises a 403 error
        return super().dispatch(request, *args, **kwargs)

class ShopProductGridView(ListView):
    template_name = "product/product-grid.html"
    paginate_by = 9

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = Product.objects.filter(
            status=ProductStatusType.draft.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["wishlist_items"] = WishlistProductModel.objects.filter(user=self.request.user).values_list(
            "product__id", flat=True) if self.request.user.is_authenticated else []
        context["category"] = ProductCategoryModel.objects.all()
        return context
    
class ShopProductDetailView(DetailView):
    template_name = "product/product-details.html"
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["is_wished"] = WishlistProductModel.objects.filter(
            user=self.request.user, product__id=product.id).exists() if self.request.user.is_authenticated else False
        reviews = ProductReviewModel.objects.filter(product=product,status=ReviewStatusType.accepted.value)
        context["reviews"] = reviews
        total_reviews_count =reviews.count()
        context["reviews_count"] = {
            f"rate_{rate}": reviews.filter(rate=rate).count() for rate in range(1, 6)
        }
        if total_reviews_count != 0:
            context["reviews_avg"] = {
                f"rate_{rate}": round((reviews.filter(rate=rate).count()/total_reviews_count)*100,2) for rate in range(1, 6)
            }
        else:
            context["reviews_avg"] = {f"rate_{rate}": 0 for rate in range(1, 6)}
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.specifications.prefetch_related()

        obj.media.prefetch_related()
        return obj

class AddOrRemoveWishlistView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        message = ""
        if product_id:
            try:
                wishlist_item = WishlistProductModel.objects.get(
                    user=request.user, product__id=product_id)
                wishlist_item.delete()
                message = "محصول از لیست علایق حذف شد"
            except WishlistProductModel.DoesNotExist:
                WishlistProductModel.objects.create(
                    user=request.user, product_id=product_id)
                message = "محصول به لیست علایق اضافه شد"

        return JsonResponse({"message": message})
    
def display_page(request, slug):
    page_config = get_object_or_404(PageConfig, slug=slug)  # فرض بر این است که یک صفحه مشخص دارید
    return render(request, 'product/display_page.html', {
        'page_config': page_config,
        'products': page_config.page_config_products.all(),
        'slug': slug,
    })
def generate_pdf(request, slug):
    # Fetch data
    page_config = get_object_or_404(PageConfig, slug=slug)  # فرض بر این است که یک صفحه مشخص دارید
    if not page_config:
        return HttpResponse("No page configuration found.", status=404)

    # Get the selected products for this page
    products = page_config.page_config_products.all()
    last_update = page_config.last_update

    # Render HTML template with context
    html_content = render_to_string('product/pdf_template.html', {
        'products': products,
        'last_update': last_update,
        'page_name': page_config.page_name,
        'logo': page_config.logo,
    })

    # Generate PDF

    pdf_file = HTML(string=html_content).write_pdf()
    
    # Return PDF as response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{page_config.page_name}.pdf"'
    return response