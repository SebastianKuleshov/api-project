from django.urls import path
from .views import PostAPI, PostAPIList

app_name = 'post'

urlpatterns = [
    path('', PostAPIList.as_view(), name='post_list'),
    path('<int:pk>/', PostAPI.as_view(), name='post_update_delete'),
]