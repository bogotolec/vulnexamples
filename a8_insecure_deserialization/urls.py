from django.urls import path
from . import views


app_name = 'a8_insecure_deserialization'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('buy/', views.buy, name='buy'),
]
