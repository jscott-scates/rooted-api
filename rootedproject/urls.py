from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rootedapi.models import *
from rootedapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", Users,"user")
router.register(r"sages",Sages, "sage")

urlpatterns = [
    path('', include(router.urls)),
]

