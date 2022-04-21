import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return baker.make(User, username="test", password=make_password("p@ssw0rd"))
