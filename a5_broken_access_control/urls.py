from django.urls import path

from . import views


app_name = 'a5_broken_access_control'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('new_note/', views.NewNoteView.as_view(), name='new_note'),
    path('note/', views.note_view, name='note'),
]
