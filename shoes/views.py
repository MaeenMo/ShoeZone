from django.shortcuts import render, redirect
import datetime
from .models import *
from .form import *
from random import randint
from django.contrib.auth.views import *
from django.contrib.admin.models import *
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib import messages

# Function To Check For URL Direct Access
def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer

def remove_search_dub(key, str):
    arr = []
    arr2 = []
    duplicate_names = Shoe.objects.filter(brand__contains=key).values('name').annotate(name_count=Count('name')).filter(name_count__gt=1)
    for name_obj in duplicate_names:
        name = name_obj['name']
        for i in Shoe.objects.filter(name=name)[1:]:
            arr.append(i)
    if str:
        for i in Shoe.objects.all().order_by(str):
            if not arr.__contains__(i):
                arr2.append(i)
    else:
        for i in Shoe.objects.all():
            if not arr.__contains__(i):
                arr2.append(i)
    return arr2

def remove_name_duplicate(str):
    arr = []
    arr2 = []
    duplicate_names = Shoe.objects.values('name').annotate(name_count=Count('name')).filter(name_count__gt=1)
    for name_obj in duplicate_names:
        name = name_obj['name']
        for i in Shoe.objects.filter(name=name)[1:]:
            arr.append(i)
    if str:
        for i in Shoe.objects.all().order_by(str):
            if not arr.__contains__(i):
                arr2.append(i)
    else:
        for i in Shoe.objects.all():
            if not arr.__contains__(i):
                arr2.append(i)
    return arr2

def correcting_img_path():
    for i in Shoe.objects.all():
        temp = str(i.img)
        if temp[:9] == "ShoeZone/":
            temp = temp[9:]
            i.img = temp
            i.save()

##########################################

def home(request):
    LogEntry.objects.all().delete()
    correcting_img_path()
    count = int(Shoe.objects.count())
    arr = [1 for i in range(count)]
    for i in range(1, count):
        arr[i] = arr[i - 1] + 1
    y = 0
    for i in Shoe.objects.all():
        i.shoe_num = arr[y]
        i.save()
        y += 1
    names = ["" for i in range(4)]
    result_list = []
    limit = 0
    for i in range(count, 0, -1):
        if Shoe.objects.get(shoe_num=i).name not in names and limit < 4:
            result_list.append(Shoe.objects.get(shoe_num=i))
            names.append(Shoe.objects.get(shoe_num=i).name)
            limit += 1
    context = {
        'home_items': result_list,
        'class_css': 'p-0 m-0 border-0 bd-example',
        'nav': True
    }
    return render(request, 'shoes/home.html', context)


variable = ""


def search_shoes(request):
    if not get_referer(request):
        raise Http404
    global variable
    if request.POST.get('searched'):
        searched = request.POST.get('searched')
        variable = searched
    elif request.POST.get('sort_criteria'):
        searched = variable
    elif request.GET.get('criteria'):
        searched = request.GET.get('criteria')
        variable = searched
    else:
        searched = ""
        variable = ""
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
    context = {
        'searched': searched,
        'page_name': 'Search Results',
        'nav': True
    }
    searched = str(searched).replace(" ", "")
    searched = searched.lower()
    if request.POST.get('sort_criteria') == 'Name (A - Z)':
        if Shoe.objects.filter(brand__contains=searched):
            context['shoes_brands'] = remove_search_dub(searched, 'name')
        else:
            arr = []
            for i in remove_name_duplicate('name'):
                if i.name.replace(' ', '').lower().__contains__(searched):
                    arr.append(i)
            context['shoes_brands'] = arr
        context['sort'] = 'Name (A - Z)'
    elif request.POST.get('sort_criteria') == 'Name (Z - A)':
        if Shoe.objects.filter(brand__contains=searched):
            context['shoes_brands'] = remove_search_dub(searched, '-name')
        else:
            arr = []
            for i in remove_name_duplicate('-name'):
                if i.name.replace(' ', '').lower().__contains__(searched):
                    arr.append(i)
            context['shoes_brands'] = arr
        context['sort'] = 'Name (Z - A)'
    elif request.POST.get('sort_criteria') == 'Price (Low - High)':
        if Shoe.objects.filter(brand__contains=searched):
            context['shoes_brands'] = remove_search_dub(searched, 'price')
        else:
            arr = []
            for i in remove_name_duplicate('price'):
                if i.name.replace(' ', '').lower().__contains__(searched):
                    arr.append(i)
            context['shoes_brands'] = arr
        context['sort'] = 'Price (Low - High)'
    elif request.POST.get('sort_criteria') == 'Price (High - Low)':
        if Shoe.objects.filter(brand__contains=searched):
            context['shoes_brands'] = remove_search_dub(searched, '-price')
        else:
            arr = []
            for i in remove_name_duplicate('-price'):
                if i.name.replace(' ', '').lower().__contains__(searched):
                    arr.append(i)
            context['shoes_brands'] = arr
        context['sort'] = 'Price (High - Low)'
    else:
        if Shoe.objects.filter(brand__contains=searched):
            context['shoes_brands'] = remove_search_dub(searched, "")
        else:
            arr = []
            for i in remove_name_duplicate(""):
                if i.name.replace(' ', '').lower().__contains__(searched):
                    arr.append(i)
            context['shoes_brands'] = arr
    return render(request, 'shoes/search_shoes.html', context)


def search_autocomp(request):
    address = request.GET.get('address')
    context = {
        'status': 200,
    }
    arr = []
    sent_arr = []
    if address:
        if Shoe.objects.filter(brand__contains=address):
            for i in Shoe.objects.filter(brand__contains=address):
                arr.append(i.brand)
        elif Shoe.objects.filter(name__contains=address):
            for i in Shoe.objects.filter(name__contains=address):
                arr.append(i.name)
    for i in arr:
        if arr.__contains__(i) and not sent_arr.__contains__(i):
            sent_arr.append(i)
    context['data'] = sent_arr
    return JsonResponse(context)


def item_page(request, item_id):
    if not get_referer(request):
        raise Http404
    for i in Shoe.objects.all():
        temp = ''
        temp = str(i.img)
        if temp[0:9] == "ShoeZone/":
            i.img = str(temp[9:])
            i.save()
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
    for i in Shoe.objects.all():
        temp = ''
        temp = str(i.img)
        if temp[0:9] == "ShoeZone/":
            i.img = str(temp[9:])
            i.save()
    msg = []
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid() and not User.objects.filter(email__contains=str(request.POST.get('email'))):
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "{x}\'s Account is Created Successfully".format(x=username))
            return redirect('login')
        else:
            if not form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                msg.append("Password Doesn't Match")
            if User.objects.filter(username__contains=str(request.POST.get('username'))):
                msg.append("Username Already Exists")
            if str(form.cleaned_data.get('username')).isnumeric():
                msg.append("Username Must Contain Letters")
            if User.objects.filter(email__contains=str(request.POST.get('email'))):
                msg.append("Email Already Exists")
        return render(request, 'shoes/registration.html', {'form': form, 'page_name': 'Sign Up', 'errors': msg})
    else:
        form = RegistrationForm()
    return render(request, 'shoes/registration.html', {'form': form, 'page_name': 'Sign Up'})


def men(request):
    LogEntry.objects.all().delete()
    correcting_img_path()
    context = {
        'sort': ' ',
        'page_name': 'Men',
        'nav': True
    }
    if request.POST.get('sort_criteria') == 'Name (A - Z)':
        context['shoes'] = remove_name_duplicate('name')
        context['sort'] = 'Name (A - Z)'
    elif request.POST.get('sort_criteria') == 'Name (Z - A)':
        context['shoes'] = remove_name_duplicate('-name')
        context['sort'] = 'Name (Z - A)'
    elif request.POST.get('sort_criteria') == 'Price (Low - High)':
        context['shoes'] = remove_name_duplicate('price')
        context['sort'] = 'Price (Low - High)'
    elif request.POST.get('sort_criteria') == 'Price (High - Low)':
        context['shoes'] = remove_name_duplicate('-price')
        context['sort'] = 'Price (High - Low)'
    else:
        context['shoes'] = remove_name_duplicate('')
    return render(request, 'shoes/men.html', context)


def women(request):
    LogEntry.objects.all().delete()
    correcting_img_path()
    context = {
        'sort': ' ',
        'page_name': 'Women',
        'nav': True
    }
    if request.POST.get('sort_criteria') == 'Name (A - Z)':
        context['shoes'] = remove_name_duplicate('name')
        context['sort'] = 'Name (A - Z)'
    elif request.POST.get('sort_criteria') == 'Name (Z - A)':
        context['shoes'] = remove_name_duplicate('-name')
        context['sort'] = 'Name (Z - A)'
    elif request.POST.get('sort_criteria') == 'Price (Low - High)':
        context['shoes'] = remove_name_duplicate('price')
        context['sort'] = 'Price (Low - High)'
    elif request.POST.get('sort_criteria') == 'Price (High - Low)':
        context['shoes'] = remove_name_duplicate('-price')
        context['sort'] = 'Price (High - Low)'
    else:
        context['shoes'] = remove_name_duplicate("")
    return render(request, 'shoes/women.html', context)

def cart(request):
    if not get_referer(request):
        raise Http404
    for i in Shoe.objects.all():
        temp = ''
        temp = str(i.img)
        if temp[0:9] == "ShoeZone/":
            i.img = str(temp[9:])
            i.save()
    total_price = 0
    context = {
        'shoes': Shoe.objects.all(),
        'cart_items': Cart_item.objects.filter(owner_id=request.user.id),
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
    if Cart_item.objects.filter(owner=request.user):
        x = randint(100000, 999999)
        for i in Cart_item.objects.filter(owner=request.user):
            i.created_at = datetime.datetime.now()
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
        for i in Cart_item.objects.filter(owner=request.user):
            temp += "Shoe Name: {x}\nShoe Brand: {q}\nSelected Color: {w}\nSelected Sizes: {z}\nQuantity: {y}\n\n".format(
                x=i.product.name,
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
            'Error': "Stop Refreshing"
        }
    return render(request, 'shoes/checkout.html', context)


def add_To_Cart(request, cart_item_id):
    if not get_referer(request):
        raise Http404
    if request.GET.get("sizeselect"):
        if Cart_item.objects.filter(product_id=cart_item_id, owner=request.user):
            check = Cart_item.objects.get(product_id=cart_item_id, owner=request.user)
            check.selected_size += ", {y}".format(y=request.GET.get("sizeselect"))
            check.product_qty += 1
            check.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        Cart_item.objects.create(owner=request.user, product_id=cart_item_id, product_qty=1)
        hh = Cart_item.objects.get(owner=request.user, product_id=cart_item_id)
        hh.selected_size = request.GET.get("sizeselect")
        hh.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
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
            if request.user.username != request.POST.get('username'):
                messages.error(request, 'Username Already Exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if User.objects.filter(email=request.POST.get('email')):
            if request.user.email != request.POST.get('email'):
                messages.error(request, 'Email Already Exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if not request.POST.get('email'):
            messages.error(request, 'Do Not Leave Email Blank')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if request.POST.get('first_name').isnumeric() or request.POST.get('last_name').isnumeric():
            messages.error(request, 'First/Last Name Can’t Be Entirely Numeric')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if not request.POST.get('first_name') or not request.POST.get('last_name'):
            messages.error(request, 'Do Not Leave First/Last Name Blank')
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


def handle404(request, exception):
    context = {
        'class_css': 'p-0 m-0 border-0 bd-example',
        'page_name': 'Shoezone 404'
    }
    return render(request, 'shoes/404.html', context)
