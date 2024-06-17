from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import PostSerializer
from .models import Post
from .permissions import IsOwnerOrAdmin
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


def index(request):
    return render(request, "index.html")


class PostAPIList(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def get(self, request):
        queryset = Post.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PostSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostAPI(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk is None:
            return Response({"error": "Method get not allowed"}, status=400)
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PostSerializer,
    )
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk is None:
            return Response({"error": "Method patch not allowed"}, status=400)
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)
        
        self.check_object_permissions(request, post)
        serializer = self.serializer_class(instance=post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PostSerializer,
    )
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk is None:
            return Response({"error": "Method delete not allowed"}, status=400)
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)
        
        self.check_object_permissions(request, post)
        post.delete()
        return Response({"message": "Post deleted successfully"})


# class PostAPIList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (IsAuthenticated,)


# class PostAPIUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (IsOwnerOrAdmin,)
