from django.contrib import admin
from django.urls import path, include


handler404 = 'vulnexamples.views.view404'

urlpatterns = [
    path('', include('index.urls')),
    path('admin/', admin.site.urls),
]
