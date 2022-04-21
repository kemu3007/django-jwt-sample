from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerailizer


class UserViewSets(ModelViewSet):
    serializer_class = UserSerailizer
    queryset: QuerySet[User] = User.objects.all()
    permission_classes = (IsAuthenticated,)
