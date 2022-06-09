from django.contrib import admin
from django.urls import path
from . import views


app_name = "sales"


urlpatterns = [
    path("", views.car_listings, name="home"),
    # path("list", views.car_listings, name="list"),
    path("list", views.CarListing.as_view(), name="list"),


    # path("sell", views.sell_car, name="sell"),
    path("sell", views.SellCar.as_view(), name="sell"),

    # path("buy/<int:pk>", views.buy_car, name="buy"),
    path("buy/<int:pk>", views.BuyCar.as_view(), name="buy"),

    # path("make-available/<int:pk>", views.make_available, name="make-available"),
    path("make-available/<int:pk>", views.MakeAvailable.as_view(), name="make-available"),

    # path("finalise-sale/<int:pk>", views.finalise_sale, name="finalise-sale"),
    path("finalise-sale/<int:pk>", views.FinaliseSale.as_view(), name="finalise-sale"),
]