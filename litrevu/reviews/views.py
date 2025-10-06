from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView


class FeedView(TemplateView, LoginRequiredMixin):
    template_name = 'reviews/feed.html'
    pass


class PostView(ListView):
    pass


class FollowView(ListView):
    pass


