from django.urls import path, include
from rest_framework import routers

from .views import CommentViewSet

router = routers.SimpleRouter()
router.register(r'', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

