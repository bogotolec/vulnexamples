from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse
from django.views.generic import View
from django.contrib.auth import get_user_model
import re
import hashlib


from vulnexamples.views import HostsLoginView, HostsRegistrationView
from .forms import AddCartForm

item_list = [
    {
        "id": 1,
        "name": "Bread",
        "description": "I am bread",
        "image": "images/bread.jpg",
        "price": 3,
    },
    {
        "id": 2,
        "name": "Sliced bread",
        "description": "I am sliced bread",
        "image": "images/sliced_bread.jpeg",
        "price": 5,
    },
    {
        "id": 3,
        "name": "Not bread",
        "description": "You may thought I were bred but I'm not bred I'm cat!!!!eat me not!!!!!",
        "image": "images/not_bread.jpg",
        "price": 15,
    },
    {
        "id": 4,
        "name": "baguette",
        "description": "délicieuse",
        "image": "images/baguette.png",
        "price": 5,
    },
]

class Cipher:

    salt = b"a i b sideli na trube"

    def encode(self, value):
        return hashlib.md5(bytes(str(value), 'ascii') + self.salt).hexdigest()

    def decode(self, value):
        for i in range(10000):
            if self.encode(i) == value:
                return i
        else:
            return None

def add_item(cookie, id):
    
    price = 0
    items = []
    block_size = 32

    c = Cipher()

    if cookie != None and cookie != "":
        price = c.decode(cookie[:block_size])
    else:
        cookie = ""
    if price == None:
        cookie = ""
    price += int(item_list[id - 1]['price'])
    cookie = c.encode(price) + cookie[32::]
    cookie += c.encode(id)

    return cookie


def index(request):
    return render(request, 'a8_insecure_deserialization/index.html')


class Cart:

    def __init__(self, cookie):
        self.price = 0
        self.items = [0] * len(item_list)

        c = Cipher()

        self.price = c.decode(cookie[:32])
        if self.price == None:
            return None

        for i in range(len(cookie) // 32 - 1):
            id = c.decode(cookie[32 * (i + 1): 32*(i+2)])

            if id == None:
                return None
            self.items[id - 1] += 1

    def cost(self):
        return self.price


    def to_string(self):
        res = []
        for i in range(len(self.items)):
            if self.items[i] != 0:
                
                t = {
                    'name': item_list[i]['name'],
                    'count': self.items[i],
                }
                res.append(t)
        return res

class ShopView(View):
    template_name = "a8_insecure_deserialization/shop.html"
    form_class = AddCartForm

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name, {"items": item_list})
        else:
            return redirect('index')

    def post(self, request):
        form = self.form_class(request.POST)

        if request.user.is_authenticated and form.is_valid():

            id = form.cleaned_data['id']

            response = render(request, self.template_name, {"items": item_list})
            response.set_cookie('cart', add_item(request.COOKIES.get('cart'), id))

            return response
        else:
            return redirect('index')


class CartView(View):
    template_name = "a8_insecure_deserialization/cart.html"

    def get(self, request):
        if request.user.is_authenticated:
            
            cart = Cart(request.COOKIES.get('cart'))
            
            if cart != None:
                response = render(request, self.template_name, {"items": cart.to_string(), "cost": cart.cost()})
            else:
                response = render(request, self.template_name)
                response.set_cookie("cart", "")

            return response
        else:
            return redirect('index')


class RegistrationView(HostsRegistrationView):
    subdomain = 'a8_insecure_deserialization'


class LoginView(HostsLoginView):
    subdomain = 'a8_insecure_deserialization'


def logout_view(request):
    logout(request)
    return redirect(reverse('index', host='a8_insecure_deserialization'))


def buy(request):
    cart = Cart(request.COOKIES.get('cart'))

    args = { 'message': [] }

    if cart == None:
        args['message'].append('unexpected error')
        response = render(request, "a8_insecure_deserialization/buy.html", args)
        response.set_cookie("cart", "")
        return response
    elif len(cart.to_string()) == 0:
        args['message'].append("Cart is empty")

    elif cart.cost() > request.user.balance:
        args['message'].append("Not enough money")

    else:
        request.user.balance -= cart.cost()
        request.user.save()
        args['message'].append("success")
        response = render(request, "a8_insecure_deserialization/buy.html", args)
        response.set_cookie("cart", "")
        return response

    return render(request, "a8_insecure_deserialization/buy.html", args)