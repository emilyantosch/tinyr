"""
URL configuration for tinyr_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewset
from matches.views import MatchViewset 
from user_profile.views import UserProfileViewset



user_router = DefaultRouter()
user_router.register(r'user', UserViewset)

match_router = DefaultRouter()
match_router.register(r'match', MatchViewset)

user_profile_router = DefaultRouter()
user_profile_router.register(r'user_profile', UserProfileViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include("image_model.urls")),
    path('profile/', include("user_profile.urls")),
    path('profile/', include(user_profile_router.urls)),
    path('users/', include("users.urls")),
    path('users/', include(user_router.urls)),
    path('matches/', include("matches.urls")),
    path('matches/', include(match_router.urls)),
]
