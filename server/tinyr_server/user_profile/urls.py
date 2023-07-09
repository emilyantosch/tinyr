from django.urls import path
from . import views

urlpatterns = [
    path("current_user_profile/", views.GetUserProfileForCurrentUser.as_view()),
    path("create_user_profile/", views.CreateUserProfile.as_view())
]
