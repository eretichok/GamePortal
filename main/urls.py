from django.contrib import admin
from django.urls import path, include
from .views import PostsList, PostDetails, ActivityList, PostCreate, PostEdit, PostDelete


urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>/', PostDetails.as_view(), name='post_detail'),
    path('user_activity/', ActivityList.as_view(), name='user_activity'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    # path('response/<int:pk>', (ResponseList.as_view()), name='posts'),

]