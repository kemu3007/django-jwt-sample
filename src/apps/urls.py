"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

import apps.views as apps_views

router = DefaultRouter()

router.register("user", apps_views.UserViewSets)

jwt_urls = [
    path("", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("verify/", TokenVerifyView.as_view()),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("token/", include(jwt_urls)),
    path("api/v1/", include(router.urls)),
]
