from typing import Dict

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class UserSerailizer(ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data: Dict[str, str]) -> User:
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
