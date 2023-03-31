from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .form import *
from random import randint, randrange
from django.urls import reverse
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login


def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer

def home(request):
    x = [None for i in range(4)]
    count = int(Shoe.objects.count())
    arr = [1 for i in range(count)]
    for i in range(1, count):
        arr[i] = arr[i-1] + 1
    y = 0
    for i in Shoe.objects.all():
        i.shoe_num = arr[y]
        i.save()
        y += 1
    temp = [count-3, count-2, count-1, count]
    for i in range(4):
        x[i] = Shoe.objects.get(shoe_num=temp[i])
    context = {
        'shoes': Shoe.objects.all(),
        'home_items': x,
        'class_css': 'p-0 m-0 border-0 bd-example',
        'nav': True
    }
    return render(request, 'shoes/home.html', context)


def search_shoes(request):
    if not get_referer(request):
        raise Http404
    searched = request.POST['searched']
    searched = str(searched).replace(" ", "")
    shoes_brands = Shoe.objects.filter(brand__contains=searched)
    context = {
        'searched': searched,
        'shoes_brands': shoes_brands,
        'page_name': 'Search Results',
        'nav': True
    }
    return render(request, 'shoes/search_shoes.html', context)


def item_page(request, myid):
    # if not get_referer(request):
    #     raise Http404
    context = {
        'shoes': Shoe.objects.filter(id=myid),
        'page_name': 'Item Page',
        'nav': True
    }
    return render(request, 'shoes/itempage.html', context)


def registration(request):
    if not get_referer(request):
        raise Http404
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account is Created Successfully")
            return redirect('login')
        else:
            messages.error(request, "Password Doesn't Match :(")
    else:
        form = RegistrationForm()
    return render(request, 'shoes/registration.html', {'form': form, 'page_name': 'Sign Up'})


def men(request):
    context = {
        'shoes': Shoe.objects.all(),
        'page_name': 'Men',
        'nav': True
    }
    return render(request, 'shoes/men.html', context)


def women(request):
    context = {
        'shoes': Shoe.objects.all(),
        'page_name': 'Women',
        'nav': True
    }
    return render(request, 'shoes/women.html', context)


def cart(request):
    if not get_referer(request):
        raise Http404
    total_price = 0
    context = {
        'shoes': Shoe.objects.all(),
        'cart_items': User_Order.objects.filter(owner_id=request.user.id),
        'page_name': 'Cart',
        'nav': False
    }
    if context['cart_items']:
        for i in context['cart_items']:
            temp = ''
            for j in i.product.price:
                if j.isnumeric():
                    temp += j
            total_price += int(temp) * i.product_qty
    total_items = context['cart_items'].count()
    context['no_items'] = int(total_items)
    context['total_price'] = total_price
    context['price_with_shipping'] = total_price + 40
    return render(request, 'shoes/shoppingcart.html', context)

def checkout(request):
    if not get_referer(request):
        raise Http404
    if User_Order.objects.all():
        for i in User_Order.objects.all():
            i.delete()
        x = randint(10000, 99999)
        context = {
            'page_name': "Checkout",
            'order_no': x
        }
    else:
        context = {
            'page_name': "Checkout",
            'Error': "Stop Refreshing :("
        }
    return render(request, 'shoes/checkout.html', context)
    # messages.success(request, "Please Fill Your Cart Then Checkout :(")
    # return redirect('cart')
def add_To_Cart(request, xid):
    if not get_referer(request):
        raise Http404
    if User_Order.objects.filter(product_id=xid):
        check = User_Order.objects.get(product_id=xid)
        check.product_qty += 1
        check.save()
        messages.success(request, "Item Already in Cart")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    messages.success(request, "Item Added To Cart")
    User_Order.objects.create(owner=request.user, product_id=xid, product_qty=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def remove_From_Cart(request, xid):
    if not get_referer(request):
        raise Http404
    if User_Order.objects.filter(product_id=xid):
        check = User_Order.objects.get(product_id=xid)
        check.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    messages.success(request, "Item Not in Cart")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

