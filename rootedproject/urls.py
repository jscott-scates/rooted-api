from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rootedapi.models import *
from rootedapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", Users,"user")
router.register(r"sages",Sages, "sage")
router.register(r"spreads", Spreads,"spread")
router.register(r"decks", Decks, "deck")
router.register(r"decktypes", DeckTypes, "decktype")
router.register(r"elements", Elements, "element")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

