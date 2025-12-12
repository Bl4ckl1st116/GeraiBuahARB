from django.shortcuts import render

# Create your views here.
from .models import Buah


def authenticated_user(request):
    return render(request, 'core/auth.html')

def index(request):
    return render(request, 'core/home.html')

def buah(request):
    buah_list = Buah.objects.all()
    return render(request, 'core/buah.html', {'buah_list': buah_list})


def keranjang(request):
    return render(request, 'core/cart.html')

def kontak(request):
    return render(request, 'core/contact.html')

def shop_detail(request):
    return render(request, 'core/shop-detail.html')