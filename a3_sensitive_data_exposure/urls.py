from django.urls import path

from . import views


app_name = 'a3_sensitive_data_explosure'

handler400 = views.view400
handler403 = views.view403
handler404 = views.view404
handler500 = views.view500

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('robots.txt', views.robots_view, name='robots'),
    path('logs.txt', views.logs_view, name='logs'),
]
