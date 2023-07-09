from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

import uuid

from users.models import User
from .models import UserProfile
from .serializer import UserProfileSerializer

# Create your views here.


class UserProfileViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class GetUserProfileForCurrentUser(APIView):
    def post(self, request):
        user = request.data["user"]

        try:
            user_object = User.objects.filter(id=user)
        except ObjectDoesNotExist:
            print("Current User is not existent")
            return HttpResponse(status=400)

        try:
            user_profile = UserProfile.objects.filter(user=user_object)
        except ObjectDoesNotExist:
            print("User does not have a profile")
            return HttpResponse(status=400)
        serializer = UserProfileSerializer(user_profile)
        return JsonResponse(serializer.data, safe=False)


class CreateUserProfile(APIView):
    def post(self, request):
        profile_data = request.data
        user = request.data["user"]

        try:
            user_object = User.objects.filter(id=user)
        except ObjectDoesNotExist:
            print("Current User is not existent")
            return HttpResponse(status=400)

        try:
            profile = UserProfile.objects.create(
                id=uuid.uuid4(),
                date_of_birth=profile_data["date_of_birth"],
                gender=profile_data["gender"],
                height=profile_data["height"],
                body_type=profile_data["body_type"],
                sexual_orientation=profile_data["sexual_orientation"],
                location=profile_data["location"],
                bio=profile_data["bio"],
                user=user_object
            )
        except RuntimeError:
            print("Failed to create profile. Aborting.")
            return HttpResponse(status=500)

        serializer = UserProfileSerializer(profile)
        return JsonResponse(serializer.data, status=200)
