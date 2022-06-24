from django.contrib import admin
from django.urls import path
from . import views
# from rest_framework.urlpatterns import format_suffix_patterns



app_name = "sales"


urlpatterns = [
    path("", views.CarListing.as_view(), name="home"),
    # path("list", views.car_listings, name="list"),
    path("list", views.CarListing.as_view(), name="list"),
    # path("sell", views.sell_car, name="sell"),
    path("sell", views.SellCar.as_view(), name="sell"),
    # path("buy/<int:pk>", views.buy_car, name="buy"),
    path("buy/<int:pk>", views.BuyCar.as_view(), name="buy"),
    # path("make-available/<int:pk>", views.make_available, name="make-available"),
    path(
        "make-available/<int:pk>", views.MakeAvailable.as_view(), name="make-available"
    ),
    # path("finalise-sale/<int:pk>", views.finalise_sale, name="finalise-sale"),
    path("finalise-sale/<int:pk>", views.FinaliseSale.as_view(), name="finalise-sale"),
    
    # celery urls
    path("celery-test", views.celery_view, name="celery-test"),
    path("timed-mail", views.timed_mail, name="timed-mail"),

    # DRF urls
    path("api-root/", views.api_root, name="api-root"),
    path("api-list", views.CarInfoList.as_view(), name="api-list"),
    # path("api-list", views.car_info_list, name="api-list"),
    path("api-detail/<int:pk>", views.CarInfoDetail.as_view(), name="api-detail"),
    # path("api-detail/<int:pk>", views.car_info_detail, name="api-detail"),
]


# we are adding this so that our application can handle any format's request,
#  as we are no longer working with single type of data, instead json, api etc.
# urlpatterns = format_suffix_patterns(urlpatterns)
