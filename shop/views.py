from django.utils import tree
from payments.paytm import generate_checksum, verify_checksum
from django.conf import settings
from shop.models import Transaction
from django.db.models import query
from django.views import View
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import fields
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django import forms
from django.contrib import messages, auth
from django.http import HttpResponse
from .models import Customer, OrderPlaced, Product, Categories, Cart, Wishlist
from .forms import AddProductForm, CustomerProfileForm
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import login, authenticate
from shop import models
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# ----------------------new-----------------------
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Q
import random


def index(request):
    products = Product.objects.all()
    items = list(Product.objects.all())
    random_items = random.sample(items, 3)

    return render(request, 'pages/index.html', {"products": products, 'random': random_items})


def shop(request):
    categories = Categories.objects.all()

    products = Product.objects.all()
    cement = Product.objects.filter(type=1)
    structural_steel = Product.objects.filter(type=2)
    reinforcement_steel = Product.objects.filter(type=3)
    bitumen = Product.objects.filter(type=4)

    context = {"categories": categories,
               "products": products,
               "cement_product": cement,
               "structural_steel": structural_steel,
               "reinforcement_steel": reinforcement_steel,
               "bitumen": bitumen,

               }
    return render(request, 'pages/shop.html', context)

# ------filter by categories----


def filterBycement(request):
    categories = Categories.objects.all()
    cement = Product.objects.filter(type=1)
    context = {"products": cement,
               "categories": categories, }
    return render(request, 'pages/shop.html', context)


def filterBystructuralsteel(request):
    categories = Categories.objects.all()
    structural_steel = Product.objects.filter(type=2)
    context = {"products": structural_steel,
               "categories": categories, }
    return render(request, 'pages/shop.html', context)


def filterByreinforcementsteel(request):
    categories = Categories.objects.all()
    reinforcement_steel = Product.objects.filter(type=3)
    context = {"products": reinforcement_steel,
               "categories": categories, }
    return render(request, 'pages/shop.html', context)


def filterBybitumen(request):
    categories = Categories.objects.all()
    bitumen = Product.objects.filter(type=4)
    context = {"products": bitumen,
               "categories": categories, }
    return render(request, 'pages/shop.html', context)


def filterByPrice0to500(request):
    product = Product.objects.filter(
        Q(discounted_price__gte=0) & Q(discounted_price__lte=500))
    context = {"products": product, }
    return render(request, 'pages/shop.html', context)


def filterByPrice500to1000(request):
    product = Product.objects.filter(
        Q(discounted_price__gte=500) & Q(discounted_price__lte=1000))
    context = {"products": product, }
    return render(request, 'pages/shop.html', context)


def filterByPrice1000to5000(request):
    product = Product.objects.filter(
        Q(discounted_price__gte=1000) & Q(discounted_price__lte=5000))
    context = {"products": product, }
    return render(request, 'pages/shop.html', context)


def filterByPrice5000to10000(request):
    product = Product.objects.filter(
        Q(discounted_price__gte=5000) & Q(discounted_price__lte=10000))
    context = {"products": product, }
    return render(request, 'pages/shop.html', context)


def search(request):

    products_list = Product.objects.all()

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            products_list = products_list.filter(
                description__icontains=keywords)
    context = {'products': products_list}
    return render(request, 'pages/shop.html', context)


def about(request):
    return render(request, 'pages/about.html', {})


@login_required(redirect_field_name="shop")
def AddToCart(request):
    user = request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("myapp:shop")


@login_required(redirect_field_name="login")
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0.00
        shipping_charge = 150.00
        total_amount = 0.00
        cart_product = [product for product in Cart.objects.all()
                        if product.user == user]

        if cart_product:
            for product in cart_product:
                product_price = (product.quantity *
                                 product.product.discounted_price)
                amount += product_price
                total_amount = amount + shipping_charge
    context = {'cart': cart,
               'amount': amount,
               'shipping_charge': shipping_charge,
               'total_amount': total_amount,
               }
    return render(request, 'pages/cart.html', context)


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['id']
        print(prod_id)
        obj = Cart.objects.get(Q(product=prod_id)
                               & Q(user=request.user))
        obj.quantity += 1
        obj.save()

        amount = 0.00
        shipping_charge = 150.00
        total_amount = 0.00
        product_amount = obj.product_cost

        cart_product = [product for product in Cart.objects.all()
                        if product.user == request.user]

        for product in cart_product:
            product_price = (product.quantity *
                             product.product.discounted_price)
            amount += product_price
            total_amount = amount + shipping_charge

        print("total amount", total_amount)
        print("product amount", product_amount)
        data = {
            'amount': amount,
            'total_amount': total_amount,
            'quantity': obj.quantity,
            'product_amount': product_amount,

        }
        print(data)
        # data_serialize = serializers.serialize('json', [data, ])

    # return JsonResponse({'data': data}, status=200)
    return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['id']
        print(prod_id)
        obj = Cart.objects.get(Q(product=prod_id)
                               & Q(user=request.user))
        obj.quantity -= 1
        obj.save()

        amount = 0.00
        shipping_charge = 150.00
        total_amount = 0.00
        product_amount = obj.product_cost
        cart_product = [product for product in Cart.objects.all()
                        if product.user == request.user]

        for product in cart_product:
            product_price = (product.quantity *
                             product.product.discounted_price)
            amount += product_price
            total_amount = amount + shipping_charge

        print("total amount", total_amount)
        data = {
            'amount': amount,
            'total_amount': total_amount,
            'quantity': obj.quantity,
            'product_amount': product_amount,

        }
        print(data)
    return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['id']
        print(prod_id)
        obj = Cart.objects.get(Q(product=prod_id)
                               & Q(user=request.user))
        obj.delete()

        amount = 0.00
        shipping_charge = 150.00
        total_amount = 0.00
        cart_product = [product for product in Cart.objects.all()
                        if product.user == request.user]

        for product in cart_product:
            product_price = (product.quantity *
                             product.product.discounted_price)
            amount += product_price
            total_amount = amount + shipping_charge

        print("total amount", total_amount)
        data = {
            'amount': amount,
            'total_amount': total_amount,
        }

    return JsonResponse(data)


@login_required(redirect_field_name="login")
def checkout(request):
    user = request.user
    add = Customer.objects.filter(User=user)
    cart_item = Cart.objects.filter(user=user)

    p_amount = 0.00
    shipping_charge = 150.00
    total_amount = 0.00

    cart_product = [product for product in Cart.objects.all()
                    if product.user == request.user]

    if cart_product:
        for product in cart_product:
            product_price = (product.quantity *
                             product.product.discounted_price)
            p_amount += product_price
        total_amount = p_amount + shipping_charge

    if request.method == "POST":
        transaction = Transaction(made_by=user, amount=total_amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'payments/redirect.html', context=paytm_params)

    context = {
        'add': add,
        'cart_item': cart_item,
        'p_amount': p_amount,
        'total_amount': total_amount
    }
    return render(request, 'pages/checkout.html', context)


@login_required(redirect_field_name="login")
def payment(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for item in cart:
        OrderPlaced(user=user, customer=customer,
                    product=item.product, quantity=item.quantity).save()
        item.delete()
    return render(request, )


@login_required(redirect_field_name="login")
def AddTowishlist(request):
    user = request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    Wishlist(user=user, product=product).save()
    return redirect("myapp:shop")


@login_required(redirect_field_name="login")
def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist = Wishlist.objects.filter(user=user)

    context = {'wishlist': wishlist}
    return render(request, 'pages/wishlist.html', context)


def remove_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['id']
        obj = Wishlist.objects.get(Q(product=prod_id)
                                   & Q(user=request.user))
        obj.delete()
        data = {
            'deleted': True
        }
    return JsonResponse(data)


@login_required(redirect_field_name="login")
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'pages/orders.html', {'order_placed': order_placed})


@login_required(redirect_field_name="login")
def profile(request):
    address = Customer.objects.filter(User=request.user)

    paginator = Paginator(address, 3)
    page = request.GET.get('page')
    paged_address = paginator.get_page(page)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            Address = form.cleaned_data['Address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']

            data = Customer(User=user, name=name, Address=Address,
                            city=city, state=state, pincode=pincode)
            data.save()

            messages.success(request, 'Address added succesfuly')
            return redirect('myapp:profile')
    else:
        form = CustomerProfileForm()
        return render(request, 'pages/profile.html', {'form': form, 'address': paged_address})


@method_decorator(login_required, name='dispatch')
class UpdateAddressView(UpdateView):
    model = models.Customer
    # fields = ['name', 'Address', 'city', 'state', 'pincode']
    form_class = CustomerProfileForm
    success_url = reverse_lazy("myapp:profile")


class DeleteAddressView(DeleteView):
    model = models.Customer
    context_object_name = 'address'
    success_url = reverse_lazy("myapp:profile")

 # -----json resonse-----
# def profile(request):
#     address = Customer.objects.filter(User=request.user)

#     if request.is_ajax == 'POST' or request.method == 'POST':
#         form = CustomerProfileForm(request.POST)
#         if form.is_valid():
#             user = request.user
#             name = form.cleaned_data['name']
#             Address = form.cleaned_data['Address']
#             city = form.cleaned_data['city']
#             state = form.cleaned_data['state']
#             pincode = form.cleaned_data['pincode']

#             data = Customer(User=user, name=name, Address=Address,
#                             city=city, state=state, pincode=pincode)
#             data.save()
#             data_serialize = serializers.serialize('json', [data, ])

#             messages.success(request, 'Address added succesfuly')
#             return JsonResponse({'data': data_serialize}, status=200)
#     else:
#         form = CustomerProfileForm()
#         return render(request, 'pages/profile.html', {'form': form, 'address': address})
# ----json respone end----


def contact(request):
    return render(request, 'pages/contact.html', {})


def registraion(request):
    if request.method == 'POST':
        # Get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

    # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('myapp:registratiion')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('myapp:registratiion')
                else:
                    # Looks good
                    user = User.objects.create_user(
                        username=username, password=password, email=email,)
                    # Login after register
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in')
                    return redirect('myapp:index')
                    # user.save()
                    # messages.success(
                    #    request, 'You are now registered and can log in')
                    # return redirect('myapp:index')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('myapp:registratiion')
    else:
        return render(request, 'pages/registration.html', {})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('myapp:index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('myapp:login')
    else:
        return render(request, 'pages/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('myapp:index')


class addProduct(CreateView):
    model = models.Product
    form_class = AddProductForm
    success_url = reverse_lazy("myapp:list_product")


class listProduct(ListView):
    model = models.Product
    context_object_name = 'products'


# class detailProduct(DetailView):
#     model = models.Product
#     template_name = 'pages/shopsingle.html'


class detailProduct(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()

        item_already_in_wishlist = False
        if request.user.is_authenticated:
            item_already_in_wishlist = Wishlist.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()

        context = {
            'product': product,
            'item_already_in_cart': item_already_in_cart,
            "item_already_in_wishlist": item_already_in_wishlist,
        }
        return render(request, 'pages/shopsingle.html', context)


class updateProduct(UpdateView):
    model = models.Product
    fields = '__all__'
    success_url = reverse_lazy("myapp:list_product")


class deleteProduct(DeleteView):
    model = models.Product
    success_url = reverse_lazy("myapp:list_product")


class addCategorie(CreateView):
    model = models.Categories
    fields = '__all__'
    success_url = reverse_lazy("myapp:list_categorie")


class listCategorie(ListView):
    model = models.Categories
    context_object_name = "categories"


class detailCategorie(DetailView):
    model = models.Categories


class deleteCategorie(DeleteView):
    model = models.Categories
    success_url = reverse_lazy("myapp:list_categorie")

# ----------------------orders management-----------


class updateOrder(UpdateView):
    model = models.OrderPlaced
    fields = ['status']
    context_object_name = "order"
    success_url = reverse_lazy("myapp:order_list")


@staff_member_required(login_url='myapp:login')
def manageOrders(request):
    order = OrderPlaced.objects.all()
    return render(request, 'shop/orderplaced_list.html', {'orders': order})
