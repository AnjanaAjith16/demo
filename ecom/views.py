from django.shortcuts import render, redirect, reverse
from django import views
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, FormView, CreateView, TemplateView, DetailView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from . forms import SignUp
from . models import Book, Cart, CartItem, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . utils import id_generator
import time
# Create your views here.


def home(request):
    book = Book.objects.all()
    return render(request,'index.html',{'book' : book})


class Contact(TemplateView):
    template_name = 'contact.html'


class SearchResultsView(ListView):
    model = Book
    template_name = 'bookcategory.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )
        return object_list


def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignUp()
    return render(request,"signup.html",{'form':form})


def all(request):
    num = Book.objects.all()
    paginator = Paginator(num, 12)
    page = request.GET.get('page')
    b = paginator.get_page(page)
    return render(request, 'booklist.html', {'item': b})


def low(request):
    sort = Book.objects.all().order_by('price')
    return render(request, 'booklist.html', {'item': sort})


def high(request):
    sort = Book.objects.all().order_by('-price')
    return render(request, 'booklist.html', {'item': sort})


class ItemDetail(DetailView):
    model = Book
    template_name = 'productpage.html'


def product(request):
    book = Book.objects.all()
    return render(request,'product.html',{'book': book})


def add_to_cart(request,slug):
    request.session.set_expiry(14000000)
    try:
        qty = request.GET.get('qty')
        update_qty = True
    except:
        pass
    try:
        the_id = request.session['cartid']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cartid'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)
    try:
        product = Book.objects.get(slug=slug)
    except Book.DoesNotExist:
        pass

    cart_prod,created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_prod.quantity = qty
    cart_prod.save()
    return HttpResponseRedirect(reverse('cart'))

def remove_from_cart(request, id):
    try:
        the_id = request.session['cartid']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse('cart'))

    cartitem = CartItem.objects.get(id=id)
    cartitem.delete()
    request.session['items_total'] = cart.cartitem_set.count()
    return HttpResponseRedirect(reverse('cart'))


def cart(request):
    try:
        the_id = request.session['cartid']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        # cartitem = CartItem.objects.get(cart=cart)
        # cart_prod, created = CartItem.objects.get_or_create(cart=cart, product=product)
        new_total = 0
        for item in cart.cartitem_set.all():
            line_total = item.product.price * item.quantity
            item.line_total = line_total
            item.save()
            new_total += line_total
        request.session['items_total'] = cart.cartitem_set.count()
        cart.total = new_total
        cart.save()
        context = {'cart': cart}
    else:
        empty_msg = "Your Cart is Empty. Please keep shopping"
        context = {"empty": True, 'empty_msg':empty_msg}
    return render(request,'cart.html',context)


def orders(request):
    context = {}
    return render(request,"user.html",context)


@login_required
def checkout(request):
    try:
        the_id = request.session['cartid']
        cart = Cart.objects.get(id=the_id)
    except Cart.DoesNotExist:
        the_id = None
        return HttpResponseRedirect(reverse("cart"))

    new_order, created = Order.objects.get_or_create(cart=cart)
    if created:
        new_order.order_id = id_generator() #str(time.time())
        new_order.save()
    new_order.user = request.user
    new_order.save()

    if new_order.status == "finished":
        # cart.delete()
        del request.session['cartid']
        del request.session['items_total']

    context = {'cart':cart}
    return render(request, "checkout.html", context)


