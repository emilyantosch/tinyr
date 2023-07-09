from rest_framework import serializers
from .models import Match

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["id", "p_a", "p_b", "p_a_fulfilled", "p_b_fulfilled", "match_time"]
