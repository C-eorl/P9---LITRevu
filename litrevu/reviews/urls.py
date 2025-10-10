from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path("", FeedView.as_view(), name='feed'),

    # url pour views follow
    path("follow/", FollowView.as_view(), name='follow'),
    path('follow_user/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path("search_user/", search_user, name="search_user"),
    # url pour views ticket
    path("tickets/create/", TicketCreateView.as_view(), name="ticket_create"),
    path("tickets/<int:ticket_id>/modify/", TicketModifyView.as_view(), name="ticket_modify"),
    path("tickets/<int:ticket_id>/delete/", TicketDeleteView.as_view(), name="ticket_delete"),
    # url pour views critique
    path("review/create/", ReviewView.as_view(), name="review_create"),
    path("review/<int:review_id>/modify/", ReviewModifyView.as_view(), name="review_create"),
    path("review/<int:review_id>/delete/", ReviewDeleteView.as_view(), name="review_create"),
]
