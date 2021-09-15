from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='home'),
    path('delete/<cityName>/', views.deleteCity, name = "deleteCity"),
]