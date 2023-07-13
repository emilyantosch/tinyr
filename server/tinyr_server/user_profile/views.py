from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.geos import Point
from django.db.models.functions import ExtractYear, ExtractMonth


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from datetime import date
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
                user=user_object,
            )
        except RuntimeError:
            print("Failed to create profile. Aborting.")
            return HttpResponse(status=500)

        serializer = UserProfileSerializer(profile)
        return JsonResponse(serializer.data, status=200)

def calcAge(date_of_birth : date) -> int:
    return relativedelta(date.today(), date_of_birth).years


class SearchUserProfilesAndOrder(APIView):
    def post(self, request):
        search_pattern = request.data
        search_distance = search_pattern["distance"]
        latitude = search_pattern["latitude"]
        longitude = search_pattern["longitude"]
        # Find the list of all entries,
        # whose distance is less then the exact location specified
        # Then order the list by distance
        # Define the expressions for calculating the distance between two points
        current_position = Point(longitude, latitude, srid=4326)
        max_height = search_pattern["height"][0]
        min_height = search_pattern["height"][1]
        max_age = search_pattern["age"][0]
        min_age = search_pattern["age"][1]
        tmp = UserProfile.objects.none()
        try:
            search_result = UserProfile.objects.filter(
                location__distance_lte=(current_position, search_distance)
            )
            for sexual_orientation in search_pattern["sexual_orientation"]:
                tmp = tmp | search_result.filter(gender=sexual_orientation)
            search_result = tmp
            tmp = UserProfile.objects.none()

            for body_type in search_pattern["body_type"]:
                tmp = tmp | search_result.filter(body_type=body_type)
            search_result = tmp
            tmp = UserProfile.objects.none()

            search_result = search_result.filter(
                height__lte=max_height, height__gte=min_height
            )
            
            search_result = search_result.annotate(
                age = calcAge("date_of_birth") 
            )
        except ObjectDoesNotExist:
            print("No more matches found")
            return HttpResponse(status=400)
