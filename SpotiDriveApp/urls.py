from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('destination/', views.destination, name='destination'),
    path('end/', views.end, name='end'),
    path('about/', views.about, name='about'),
]
