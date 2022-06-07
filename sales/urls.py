from django.contrib import admin
from django.urls import path, include
from . import views


app_name = "sales"


urlpatterns = [
    path("", views.car_listings, name="home"),
    path("list", views.car_listings, name="list"),
    path("sell", views.sell_car, name="sell"),
    path("buy/<int:pk>", views.buy_car, name="buy"),
    path("make-available/<int:pk>", views.make_available, name="make-available"),
    path("finalise-sale/<int:pk>", views.finalise_sale, name="finalise-sale"),
]
