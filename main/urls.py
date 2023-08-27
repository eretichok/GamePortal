from django.contrib import admin
from django.urls import path, include
from .views import PostsList, PostDetails, UserActivity
from .views import PostCreate, PostEdit, PostDelete
from .views import ResponseEdit, ResponseDelete, response_accept_change
from .views import ProfileView, ProfileEditView


urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>/', PostDetails.as_view(), name='post_details'),
    path('user_activity/', UserActivity.as_view(), name='user_activity'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('response/<int:pk>/edit/', ResponseEdit.as_view(), name='response_edit'),
    path('response/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('response/<int:pk>/accept_change/', response_accept_change, name='response_accept_change'),
    # path('response/<int:pk>/refuse/', response_refuse, name='response_refuse'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:id>/', ProfileEditView.as_view(), name='profile_edit'),

]