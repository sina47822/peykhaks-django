from django.db import models

from product.models import Product
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg
# Create your models here.
from website.models import Post  # or wherever your Post model is located

class ReviewStatusType(models.IntegerChoices):
    pending = 1, "در انتظار تایید"
    accepted = 2, "تایید شده"
    rejected = 3, "رد شده"


class ProductReviewModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(default=5, validators=[
                               MinValueValidator(0), MaxValueValidator(5)])
    status = models.IntegerField(
        choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
    
    def __str__(self):
        return f"{self.name} - {self.product.id}"
    
    
    def get_status(self):
        return {
            "id":self.status,
            "title":ReviewStatusType(self.status).name,
            "label":ReviewStatusType(self.status).label,
        }
        
        
@receiver(post_save,sender=ProductReviewModel)
def calculate_avg_review(sender,instance,created,**kwargs):
    if instance.status == ReviewStatusType.accepted.value:
        product = instance.product
        average_rating = ProductReviewModel.objects.filter(product=product, status=ReviewStatusType.accepted).aggregate(Avg('rate'))['rate__avg']
        product.avg_rate = round(average_rating,1)
        product.save()

class PostReviewModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(
        default=5,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    status = models.IntegerField(
        choices=ReviewStatusType.choices,
        default=ReviewStatusType.pending.value
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.name} - {self.post.id}"

    def get_status(self):
        return {
            "id": self.status,
            "title": ReviewStatusType(self.status).name,
            "label": ReviewStatusType(self.status).label,
        }

# Signal to update avg_rate on the Post model
@receiver(post_save, sender=PostReviewModel)
def calculate_avg_review_for_post(sender, instance, created, **kwargs):
    """
    After a review is saved (and if it is accepted),
    recalculate and update the average rating for the associated Post.
    """
    if instance.status == ReviewStatusType.accepted.value:
        post = instance.post
        average_rating = PostReviewModel.objects.filter(
            post=post,
            status=ReviewStatusType.accepted.value
        ).aggregate(Avg('rate'))['rate__avg'] or 0
        # If you've added avg_rate field to Post:
        post.avg_rate = round(average_rating, 1)
        post.save()