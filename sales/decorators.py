from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import CarInfo




def superuser_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not a super user. Please login as one to make cars available")
    return wrapper_func




def car_availability_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        car_listing = CarInfo.objects.get(id=kwargs["pk"])
        if not car_listing.sold:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("This car is no longer availble for sale.")
    return wrapper_func