from django.urls import path
from . import views

urlpatterns = [
    path("match_for_user/", views.GetAllMatchesForUser.as_view()),
    path("match_fullfilled/", views.WillMatchBeFullfilled.as_view()),
]
