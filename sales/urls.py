from django.contrib import admin
from django.urls import path, include
from . import views 


app_name = "sales"


urlpatterns = [
    path("", views.car_listings, name="home"),
    path("list", views.car_listings, name="list"),
    path("sell", views.sell, name="sell"),
    # path("/offer/<slug>", views.index, name="buy"),
]
