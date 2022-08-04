from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

# from .models import Scenario

user = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = user
        fields = ("id", "email", "name", "password")


# class ScenarioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Scenario
#         fields = '__all__'
