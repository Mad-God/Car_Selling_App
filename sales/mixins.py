from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, HttpResponse
from django.contrib.auth.models import Permission
from rest_framework import permissions


class SuperUserRequired(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        breakpoint()
        return self.request.user.is_superuser

    def handle_no_permission(self):
        breakpoint()
        return HttpResponse("You are not a super user. Please login as one to make cars available")



# class SuperUserRequired(LoginRequiredMixin, UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_superuser

#     def handle_no_permission(self):

#         return HttpResponse("You are not a super user. Please login as one to make cars available")

