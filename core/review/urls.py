from django.urls import path,re_path
from . import views

app_name = "review"

urlpatterns = [
    path("submit-review/",views.SubmitReviewView.as_view(),name="submit-review"),
    path("submit-post-review/",views.submit_post_review,name="submit-post-review")

]