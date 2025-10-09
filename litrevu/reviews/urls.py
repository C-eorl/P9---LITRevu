from django.urls import path

from .views import FeedView, FollowView, follow_user, unfollow_user, search_user

app_name = 'reviews'

urlpatterns = [
    path("", FeedView.as_view(), name='feed'),

    path("follow/", FollowView.as_view(), name='follow'),
    path('follow_user/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path("search_user/", search_user, name="search_user"),
]
