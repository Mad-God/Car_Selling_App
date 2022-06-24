from django.contrib import admin
from django.urls import path, include
from base import views as base_views
from sales.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




# Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email',]


# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path("admin/", admin.site.urls),
    # authentication urls
    # path("login/", base_views.login, name="login"),
    path("login/", base_views.LoginPageView.as_view(), name="login"),
    # path("logout/", base_views.logout, name="logout"),
    path("logout/", base_views.Logout.as_view(), name="logout"),
    # path("signup/", base_views.signup, name="signup"),
    path("signup/", base_views.SignupView.as_view(), name="signup"),
    # sales urls
    path("", include("sales.urls", namespace="")),


    # rest framework
    # token auth
    path('api-token-auth/', auth_views.obtain_auth_token),
    # jwt auth
    # path('api-jwt-token/', auth_views.Token.as_view(), name='token_obtain_pair'),
    path('api-jwt-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-jwt-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api-auth/', include('rest_framework.urls')),
    # path('user-api-url', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # tokens

]


# we are adding this so that our application can handle any format's request,
#  as we are no longer working with single type of data, instead json, api etc.
urlpatterns = format_suffix_patterns(urlpatterns)
