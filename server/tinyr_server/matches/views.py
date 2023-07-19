from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import uuid
import datetime
from itertools import chain

from users.models import User
from matches.models import Match
from .serializer import MatchSerializer

# Create your views here.


class MatchViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class WillMatchBeFullfilled(APIView):
    def post(self, request):
        partner = request.data["partner"]
        user = request.data["user"]
        try:
            user_object = User.objects.filter(id=user)
        except ObjectDoesNotExist:
            print("No User found")
            return HttpResponse(status=400)

        try:
            partner_object = User.objects.filter(id=partner)
        except ObjectDoesNotExist:
            print("Partner not found")
            return HttpResponse(status=400)

        try:
            match = Match.objects.filter(p_a=partner_object)
        except ObjectDoesNotExist:
            print("No Match has been found.")
            match = Match.objects.create(
                id=uuid.uuid4(),
                p_a=user_object,
                p_b=partner_object,
                p_a_fullfilled=True,
                p_b_fullfilled=False,
                match_time=datetime.datetime.now(),
            )

        serializer = MatchSerializer(match, many=False)
        return JsonResponse(serializer.data, safe=False)


class GetAllMatchesForUser(APIView):
    def post(self, request):
        user = request.data["user"]
        try:
            user_object = User.objects.filter(id=user)
        except ObjectDoesNotExist:
            print("The user sent was not found")
            return HttpResponse(status=400)

        all_matches = None
        try:
            all_matches = Match.objects.filter(p_a=user_object)
        except ObjectDoesNotExist:
            print("No matches have been found")

        try:
            if all_matches is None:
                all_matches = Match.objects.filter(p_b=user_object)
            else:
                all_matches = list(
                    chain(all_matches, Match.objects.filter(p_b=user_object))
                )
        except ObjectDoesNotExist:
            print("No matches have been found")

        serializer = MatchSerializer(all_matches)

        return JsonResponse(serializer.data, safe=False)
