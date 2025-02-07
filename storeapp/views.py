from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from .models import *
from .forms import *


def index(request):
    return render(request, 'index.html')
def products_view(request):
    products = TovarModel.objects.all()
    categories = CategoryModel.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'products.html', context)

def category(request, pk):
    category = CategoryModel.objects.get(id=pk)
    products = TovarModel.objects.filter(category=category)
    categories = CategoryModel.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'products.html', context)


def registeruserview(request):
    form = UserRigistrForm
    if request.method == 'POST':
        form = UserRigistrForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            Userprofile.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email
            )
            return redirect('profile')
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


def userprorfileview(request):
    profile = Userprofile.objects.get(user=request.user)
    baskets = BasketModl.objects.filter(owner=profile, ordered=False)
    baskets_summa = 0

    for basket in baskets:
        baskets_summa += basket.count * basket.product.price

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        image = request.FILES.get('image')
        profile.first_name = first_name
        profile.last_name = last_name
        profile.image = image
        profile.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    context = {
        'baskets': baskets,
        'profile': profile,
        'baskets_summa': baskets_summa
    }
    return render(request, 'users/profile.html', context)


def loginuserview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
    return render(request, 'users/login.html')


def logoutuser(request):
    logout(request)
    return redirect('home')


def add_basket_view(request, pk):
    try:
        owner = request.user.userprofile
        product = TovarModel.objects.get(id=pk)
        basket = BasketModl.objects.filter(product=product, owner=owner, ordered=False)
        if not basket:
            BasketModl.objects.create(
                product=product,
                owner=owner
            )
        else:
            basket = basket[0]
            basket.count += 1
            basket.save()
            return redirect('products')
    except:
        return redirect('loginuser')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_basket_view(request, pk):
    basket = BasketModl.objects.get(id=pk)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def create_oreder_view(request):
    profile = Userprofile.objects.get(user=request.user)
    baskets = BasketModl.objects.filter(owner=profile, ordered=False)
    baskets_summa = 0

    for basket in baskets:
        baskets_summa += basket.count * basket.product.price

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        order = OrderModel.objects.create(
            owner=profile,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            summa=baskets_summa
        )
        order.basket.set(baskets)
        order.save()
        for basket in baskets:
            basket.ordered = True
            basket.save()
        return redirect('success')

    context = {
        'baskets': baskets,
        'profile': profile,
        'baskets_summa': baskets_summa
    }
    return render(request, 'orders/order-create.html', context)


def success_view(request):
    return render(request, 'orders/success.html')

def orders_view(request):
    profile = request.user.userprofile
    orders = OrderModel.objects.filter(owner=profile)

    context = {
        'orders': orders,

    }
    return render(request, 'orders/orders.html', context)

def order_single_view(request, pk):
    order = OrderModel.objects.get(id=pk)
    context = {
        'order':order
    }

    return render(request, 'orders/order.html', context)


def adminpanel(request):
    if request.user.is_staff:
        orders = OrderModel.objects.all().order_by('-created')
        context = {
            'orders': orders
        }
        return render(request, 'admin.html', context)
    else:
        return redirect('home')


def change_status(request, pk):
    if request.user.is_staff:
        order = OrderModel.objects.get(id=pk)
        if request.method == 'POST':
            status = request.POST.get('status')
            order.status = status
            order.save()
            return redirect('admin_panel')
        context = {
            'order': order,
            'form_key': 'change'
        }
        return render(request, 'forms.html', context)
    else:
        return redirect('home')


def edit_order(request, pk):
    if request.user.is_staff:
        order = OrderModel.objects.get(id=pk)
        form = OrderForm(instance=order)
        if request.method == 'POST':
            form = OrderForm(instance=order, data=request.POST, files=request.FILES)

        context = {
            'order': order,
            'form': form,
            'form_key': 'edit'
        }
        return render(request, 'forms.html', context)
    else:
        return redirect('home')


def delete_order_view(request, pk):
    if request.user.is_staff:
        order = OrderModel.objects.get(id=pk)
        order.delete()
        return redirect('admin_panel')
    else:
        return redirect('home')


def order_category_view(request, status):
    if request.user.is_staff:
        if status == 'None':
            orders = OrderModel.objects.filter(status=None).order_by('-created')
        else:
            orders = OrderModel.objects.filter(status=status).order_by('-created')
        context = {
            'orders': orders
        }
        return render(request, 'admin.html', context)
    else:
        return redirect('home')
