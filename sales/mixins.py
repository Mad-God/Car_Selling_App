from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, HttpResponse
from rest_framework import permissions
from .models import CarInfo



class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponse("You are not a super user. Please login as one to make cars available")




class CarAvailabilityRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return CarInfo.objects.get(id=self.kwargs["pk"]).status == "available"

    def handle_no_permission(self):
        return HttpResponse("This car is no longer available")


class NotOwnCarMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return CarAvailabilityRequiredMixin.test_func(self) and not CarInfo.objects.get(id=self.kwargs["pk"]).owner == self.request.user

    def handle_no_permission(self):
        return HttpResponse("This is your own car, baka.")

