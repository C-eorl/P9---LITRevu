from django.urls import path

from .views import FeedView

app_name = 'reviews'

urlpatterns = [
    path("", FeedView.as_view(), name='feed'),
]
