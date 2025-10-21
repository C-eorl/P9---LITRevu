from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path("", FeedView.as_view(), name='feed'),
    path("posts/", PostView.as_view(), name='posts'),

    # url pour views follow
    path("follow/", FollowView.as_view(), name='follow'),
    path('follow_user/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('blocked/<int:user_id>/', blocked_user, name='blocked_user'),
    path('unblocked/<int:user_id>/', unblocked_user, name='unblocked_user'),
    path("search_user/", search_user, name="search_user"),
    # url pour views ticket
    path("tickets/create/", TicketCreateView.as_view(), name="ticket_create"),
    path("tickets/<int:pk>/modify/", TicketUpdateView.as_view(), name="ticket_modify"),
    path("tickets/<int:pk>/delete/", TicketDeleteView.as_view(), name="ticket_delete"),
    # url pour views critique
    path("review/create/", ReviewCreateView.as_view(), name="review_create"),
    path("review/create/<int:ticket_id>/", ReviewCreateView.as_view(), name="review_create_for_ticket"),
    path("review/<int:pk>/modify/", ReviewUpdateView.as_view(), name="review_modify"),
    path("review/<int:pk>/delete/", ReviewDeleteView.as_view(), name="review_delete"),
]
