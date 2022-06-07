from django.contrib import admin
from django.urls import path, include
from sales import views as sale_views
from base import views as base_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # authentication urls
    path('login/', base_views.login,name = 'login'),
    path('logout/', base_views.logout,name = 'logout'),
    path('signup/', base_views.signup,name = 'signup'),

    # sales urls
    path('', include('sales.urls', namespace = '')),
]