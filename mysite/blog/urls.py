from django.urls import path

from .views import BlogAPIList, BlogAPIDetailView

urlpatterns = [
    path('', BlogAPIList.as_view(), name='blog-list'),
    path('<int:pk>/', BlogAPIDetailView.as_view(), name='blog-detail'),
]