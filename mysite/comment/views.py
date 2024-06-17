from django.shortcuts import render
from rest_framework import viewsets, generics
from post.permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer
from .models import Comment


# Create your views here.

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrAdmin, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)