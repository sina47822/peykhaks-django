from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SubmitReviewForm
from .models import ProductReviewModel
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from .forms import SubmitPostReviewForm
from website.models import Post
from .models import ReviewStatusType

class SubmitReviewView(LoginRequiredMixin, CreateView):
    http_method_names = ["post"]
    model = ProductReviewModel
    form_class = SubmitReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        # Assuming your form has a 'product_slug' field
        product = form.cleaned_data['product']
        messages.success(self.request,"دیدگاه شما با موفقیت ثبت شد و پس از بررسی نمایش داده خواهد شد")
        return redirect(reverse_lazy('product:productdetails',kwargs={"slug":product.slug}))
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request,error)
        return redirect(self.request.META.get('HTTP_REFERER'))

def submit_post_review(request):
    """
    A simple view to handle the 'POST' submission of the review form.
    """
    if request.method == 'POST':
        form = SubmitPostReviewForm(request.POST)
        if form.is_valid():
            # By default, set the review status to "pending"
            review = form.save(commit=False)
            review.status = ReviewStatusType.pending.value  # or accepted if no moderation is needed
            review.save()
            # Redirect back to the detail page of that specific post
            return redirect(review.post.get_absolute_url())  # or however you define the detail URL
        else:
            # If form is not valid, you might want to return to the post page with errors
            # This is optional logic
            post_id = request.POST.get('post')
            return redirect(reverse('website:blog-detail', kwargs={'slug': Post.objects.get(pk=post_id).slug}))
    else:
        return redirect('website:blog-list')  # or any fallback if someone hits GET on this view