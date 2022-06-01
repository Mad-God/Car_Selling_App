from django.contrib import admin
from django.urls import path, include
from sales import views as sale_views
from . import views as u_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', sale_views.index,name = 'listings'),
    path('', include('sales.urls', namespace = '')),

    # authentication urls
    path('login/', u_views.login,name = 'login'),
    path('logout/', u_views.logout,name = 'logout'),
    path('signup/', u_views.signup,name = 'signup'),
]