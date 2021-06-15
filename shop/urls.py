from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),
    path('products/<int:myid>', views.productview, name='productview'),
    path('tracker/', views.tracker, name='tracker'),
    path('checkout/', views.checkout, name='checkout'),
]
