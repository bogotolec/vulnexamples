from django.urls import path

from . import views


app_name = 'a4_xxe'

urlpatterns = [
    path('settings.xml', views.settings, name='settings'),
    path('', views.IndexView.as_view(), name='index'),
]
