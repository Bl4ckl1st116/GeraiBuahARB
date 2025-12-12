from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.authenticated_user, name='auth'),
    path('shop/', views.buah, name='buah'),
    path('shop-detail/', views.shop_detail, name='shop-detail'),
    path('cart/', views.keranjang, name='keranjang'),
    path('contact/', views.kontak, name='kontak'),
]