from django.contrib import admin
from django.urls import path, include
from .views import PostsList   #, PostDetail, ActivityList, PostCreate


urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    # path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    # path('user_activity/', ActivityList.as_view(), name='user_activity'),
    # path('create/', PostCreate.as_view(), name='post_create'),
    # path('response/<int:pk>', (ResponseList.as_view()), name='posts'),

]