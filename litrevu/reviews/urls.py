from django.urls import path

from .views import FeedView, FollowView, follow_user, unfollow_user

app_name = 'reviews'

urlpatterns = [
    path("", FeedView.as_view(), name='feed'),
    path("follow/", FollowView.as_view(), name='follow'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('follow_user/', follow_user, name='follow_user'),

]
