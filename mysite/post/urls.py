from django.urls import path
from .views import PostAPIList, PostAPIUpdateDelete

app_name = 'post'

urlpatterns = [
    path('', PostAPIList.as_view(), name='post_list'),
    path('<int:pk>/', PostAPIUpdateDelete.as_view(), name='post_update_delete'),
]