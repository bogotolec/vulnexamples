from django.urls import path

from . import views


app_name = 'a6_security_misconfiguration'

handler404 = views.view404
handler500 = views.view500

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
