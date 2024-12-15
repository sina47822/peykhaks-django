from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('<int:order_id>/pdf/', views.generate_pdf, name='order_generate_pdf'),
]