from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerailizer


class UserViewSets(ModelViewSet):
    serializer_class = UserSerailizer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
