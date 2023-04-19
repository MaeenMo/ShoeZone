from django.shortcuts import render, redirect
import datetime
from .models import *
from .form import *
from random import randint
from django.contrib.auth.views import *
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages

# Function To Check For URL Direct Access
def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer
##########################################

def home(request):
    x = [None for i in range(4)]
    count = int(Shoe.objects.count())
    arr = [1 for i in range(count)]
    for i in range(1, count):
        arr[i] = arr[i - 1] + 1
    y = 0
    for i in Shoe.objects.all():
        i.shoe_num = arr[y]
        i.save()
        y += 1
    temp = [count - 3, count - 2, count - 1, count]
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
    searched = searched.lower()
    if searched.__contains__("nike"):
        searched = "Nike"
    elif searched.__contains__("adidas"):
        searched = "Adidas"
    elif searched.__contains__("balenciaga"):
        searched = "Balenciaga"
    elif searched.__contains__("newbalance") or searched.__contains__("new balance"):
        searched = "New Balance"
    elif searched.__contains__("converse"):
        searched = "Converse"
    shoes_brands = Shoe.objects.filter(brand__contains=searched)
    context = {
        'searched': searched,
        'shoes_brands': shoes_brands,
        'page_name': 'Search Results',
        'nav': True
    }
    return render(request, 'shoes/search_shoes.html', context)


def item_page(request, item_id):
    if not get_referer(request):
        raise Http404
    context = {
        'shoes': Shoe.objects.filter(id=item_id),
        'page_name': 'Item Page',
        'nav': True
    }
    x = []
    x = Shoe.objects.filter(name=Shoe.objects.get(id=item_id).name)
    if x.count() > 1:
        context["more_items"] = x
    else:
        context["more_items"] = []
    return render(request, 'shoes/itempage.html', context)


def registration(request):
    if not get_referer(request):
        raise Http404
    msg = []
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid() and not User.objects.filter(email__contains=str(request.POST.get('email'))):
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "{x} is Created Successfully".format(x=username))
            return redirect('login')
        else:
            if not form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                msg.append("Password Doesn't Match :(")
            if User.objects.filter(username__contains=str(request.POST.get('username'))):
                msg.append("Username Already Exists :(")
            if str(form.cleaned_data.get('username')).isnumeric():
                msg.append("Username Must Contain Letters :(")
            if User.objects.filter(email__contains=str(request.POST.get('email'))):
                msg.append("Email Already Exists :(")
        return render(request, 'shoes/registration.html', {'form': form, 'page_name': 'Sign Up', 'errors': msg})
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
        'cart_items': Cart_item.objects.filter(owner_id=request.user.id, ordered=False),
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
    price = str(total_price)
    if 1000 <= total_price <= 9999:
        price = "{x},{y}".format(x=price[0], y=price[1:])
    elif 9999 < total_price <= 99999:
        price = "{x},{y}".format(x=price[0:2], y=price[2:])
    elif total_price > 99999:
        price = "{x},{y}".format(x=price[0:3], y=price[3:])
    total_items = context['cart_items'].count()
    context['no_items'] = int(total_items)
    context['total_price'] = price
    return render(request, 'shoes/shoppingcart.html', context)


def checkout(request):
    if not get_referer(request):
        raise Http404
    total_price = 0
    if Cart_item.objects.filter(ordered=False, owner=request.user):
        x = randint(100000, 999999)
        for i in Cart_item.objects.filter(owner=request.user, ordered=False):
            i.ordered = True
            i.created_at = datetime.datetime.now()
            i.order_num = "#{h}".format(h=x)
            i.save()
            temp_p = ''
            for j in i.product.price:
                if j.isnumeric():
                    temp_p += j
            total_price += int(temp_p) * i.product_qty
        price = str(total_price)
        if 1000 <= total_price <= 9999:
            price = "{x},{y}".format(x=price[0], y=price[1:])
        elif 9999 < total_price <= 99999:
            price = "{x},{y}".format(x=price[0:2], y=price[2:])
        elif total_price > 99999:
            price = "{x},{y}".format(x=price[0:3], y=price[3:])
        temp = ""
        for i in Cart_item.objects.filter(owner=request.user, ordered=True):
            temp += "Shoe Name: {x}\nShoe Brand: {q}\nSelected Color: {w}\nSelected Sizes: {z}\nQuantity: {y}\n\n".format(x=i.product.name,
                                                                                                     q=i.product.brand,
                                                                                                     w=i.product.color,
                                                                                                     z=i.selected_size,
                                                                                                     y=i.product_qty)
            i.delete()
        Order.objects.create(order_no="#{z}".format(z=x), items=temp)
        other = Order.objects.get(order_no="#{h}".format(h=x))
        other.user_ordered = "{x} {y}".format(x=str(request.user.first_name), y=str(request.user.last_name))
        other.total_price = "EGP " + price
        other.save()
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


def add_To_Cart(request, cart_item_id):
    if not get_referer(request):
        raise Http404
    if request.POST.get("sizeselect"):
        if Cart_item.objects.filter(product_id=cart_item_id, ordered=False, owner=request.user):
            check = Cart_item.objects.get(product_id=cart_item_id, owner=request.user)
            check.selected_size += ", {y}".format(y=request.POST.get("sizeselect"))
            check.product_qty += 1
            check.save()
            messages.success(request, "Item Already in Cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        Cart_item.objects.create(owner=request.user, product_id=cart_item_id, product_qty=1)
        messages.success(request, "Item Added To Cart")
        hh = Cart_item.objects.get(owner=request.user, product_id=cart_item_id)
        hh.selected_size = request.POST.get("sizeselect")
        hh.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.success(request, "Please Select a Size")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def additional_size(request, product_id, add_size_id):
    check = Cart_item.objects.get(product_id=product_id, owner=request.user)
    check.selected_size += ", {y}".format(y=add_size_id)
    check.product_qty += 1
    check.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def remove_From_Cart(request, delete_item_id):
    if not get_referer(request):
        raise Http404
    if Cart_item.objects.filter(product_id=delete_item_id, owner=request.user):
        check = Cart_item.objects.get(product_id=delete_item_id, owner=request.user)
        check.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    messages.success(request, "Item Not in Cart")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_quantity(request, remove_quantity_id):
    if not get_referer(request):
        raise Http404
    temp = Cart_item.objects.get(product_id=remove_quantity_id, owner=request.user)
    if Cart_item.objects.filter(product_id=remove_quantity_id, owner=request.user) and temp.selected_size.__contains__(','):
        check = Cart_item.objects.get(product_id=remove_quantity_id, owner=request.user)
        check.product_qty -= 1
        i = len(check.selected_size) - 1
        x = str(check.selected_size)[:i-3]
        check.selected_size = x
        check.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    elif not temp.selected_size.__contains__(','):
        remove_From_Cart(request, temp.product_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class PasswordChange(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('login')


def profile(request):
    msg = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if User.objects.filter(username=request.POST.get('username')):
            if request.user.username == request.POST.get('username'):
                pass
            else:
                messages.error(request, 'Username Already Exists :(')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if request.POST.get('first_name').isnumeric() or request.POST.get('last_name').isnumeric():
            messages.error(request, 'First/Last Name Can’t Be Entirely Numeric :(')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if not request.POST.get('first_name') or not request.POST.get('last_name'):
            messages.error(request, 'Do Not Leave First/Last Name Blank :(')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            if form.is_valid():
                form.save()
                msg = 'Data has been saved'
    form = ProfileForm(instance=request.user)
    context = {
        'user': request.user,
        'class_css': 'p-0 m-0 border-0 bd-example',
        'nav': True,
        'form': form,
        'msg': msg
    }
    return render(request, 'shoes/profile.html', context)
