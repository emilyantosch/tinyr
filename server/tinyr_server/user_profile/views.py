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
    """
    API viewset for user profiles
    """

    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class GetUserProfileForCurrentUser(APIView):
    """
    API view for getting the user profile for the current user
    """

    def post(self, request):
        """
        Handle a POST request to get the user profile for the current user.
        """
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
    """
    API view for creating user profiles
    """

    def post(self, request):
        """
        Handle a POST request to create a user profile.
        """
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


def calc_age_from_date(date_of_birth: date) -> int:
    """
    Calculate the age of the user based on their date of birth.
    """
    return relativedelta(date.today(), date_of_birth).years


def calc_min_date_from_age(age: int) -> date:
    """
    Calculate the minimum birthdate based on the given age.

    Args:
        age: The age to calculate the minimum birthdate for.

    Returns:
        The minimum birthdate as a date object.
    """
    return date.today() - relativedelta(years=age)


class SearchUserProfilesAndOrder(APIView):
    """
    API view for searching user profiles and ordering the results.
    """

    def post(self, request):
        """
        Handle a POST request to search user profiles and order the results.

        Args:
            request: The HTTP request object.

        Returns:
            The HTTP response object.
        """
        # Save body of request as variable
        search_pattern = request.data
        # Find distance set in search_patter
        search_distance = search_pattern["distance"]
        # Get current latitude and longitude of position
        latitude = search_pattern["latitude"]
        longitude = search_pattern["longitude"]
        # Save current position on call in a Point
        current_position = Point(longitude, latitude, srid=4326)
        # Save the upper and lower limit of height
        max_height = (
            search_pattern["height"][0]
            if search_pattern["height"][0] is not None
            else None
        )
        min_height = (
            search_pattern["height"][1]
            if search_pattern["height"][0] is not None
            else None
        )

        # Save the upper and lower limit of age
        max_age = calc_min_date_from_age(search_pattern["age"][0])
        min_age = calc_min_date_from_age(search_pattern["age"][1])
        tmp = UserProfile.objects.none()
        search_result = UserProfile.objects.none()

        try:
            if (
                search_distance is not None
                or latitude is not None
                or longitude is not None
            ):
                search_result = UserProfile.objects.filter(
                    location__distance_lte=(current_position, search_distance)
                )
            if search_pattern["sexual_orientation"] is not None:
                for sexual_orientation in search_pattern["sexual_orientation"]:
                    tmp = tmp | search_result.filter(gender=sexual_orientation)
            search_result = tmp
            tmp = UserProfile.objects.none()
            if search_pattern["body_type"] is not None:
                for body_type in search_pattern["body_type"]:
                    tmp = tmp | search_result.filter(body_type=body_type)

            search_result = tmp
            tmp = UserProfile.objects.none()
            if max_height is not None or min_height is not None:
                search_result = search_result.filter(
                    height__lte=max_height, height__gte=min_height
                )
            if max_age is not None or min_age is not None:
                search_result = search_result.filter(
                    date_of_birth__lte=max_age, date_of_birth__gte=min_age
                )
        except Exception as e:
            print(f"The function encountered an issue. Error: {e}")
            return HttpResponse(status=400)

        serializer = UserProfileSerializer(search_result, many=True)
        return JsonResponse(serializer.data, status=200, safe=True)
