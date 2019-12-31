from django.urls import path
from django.contrib.auth import views
from django import views
from . import views
from django.views.generic import ListView,DetailView
from . models import Book
from . views import all,home,checkout,orders,Contact ,low,high,ItemDetail,product,cart, signup,SearchResultsView,add_to_cart,remove_from_cart

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.all, name='books'),
    path('booklow/', views.low, name='low'),
    path('bookhigh/', views.high, name='high'),

    path('products/', views.product, name='product'),
    path('product/<slug>/', ItemDetail.as_view(),name='product'),

    path('fictionn', ListView.as_view(queryset=Book.objects.filter(category__startswith='Fiction'),template_name="bookcategory.html"), name='fiction'),
    path('fantasy',ListView.as_view(queryset=Book.objects.filter(category__startswith="Fantasy"),template_name="bookcategory.html"),name='fantasy'),
    path('children',ListView.as_view(queryset=Book.objects.filter(category__startswith="Children"),template_name="bookcategory.html"),name='children'),
    path('self-help',ListView.as_view(queryset=Book.objects.filter(category__startswith="Self"),template_name="bookcategory.html"),name='self'),
    path('textbook',ListView.as_view(queryset=Book.objects.filter(category__startswith="Textbook"),template_name="bookcategory.html"),name='textbook'),

    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('contact/', Contact.as_view(), name='contact'),

    path('signup/', views.signup, name='signup'),

    path('cart/', views.cart,name='cart'),
    path('cart/<int:id>/', views.remove_from_cart, name='removefromcart'),
    path('cart/<slug>/', views.add_to_cart,name='updatecart'),
    path('checkout/', views.checkout,name='checkout'),
    path('orders/', views.orders,name='user_orders'),





]