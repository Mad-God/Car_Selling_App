from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import CarInfo


def superuser_required(view_func):
    """
    checks that the current request user is a superuser
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse(
                "You are not a super user. Please login as one to make cars available"
            )

    return wrapper_func


def car_availability_required(view_func):
    """
    checks that the current car_info record has a status of available
    """

    def wrapper_func(request, *args, **kwargs):
        car_listing = CarInfo.objects.get(id=kwargs["pk"])
        if car_listing.status == "available":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("This car is no longer available for sale.")

    return wrapper_func


def not_own_car(view_func):
    """
    checks that the current car_info record's owner and the request user are not same
    """

    def wrapper_func(request, *args, **kwargs):
        car_listing = CarInfo.objects.get(id=kwargs["pk"])
        if not car_listing.owner == request.user:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("This is your own car idiot.")

    return wrapper_func
