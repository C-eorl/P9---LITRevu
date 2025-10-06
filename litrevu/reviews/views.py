from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView


class FeedView(LoginRequiredMixin, TemplateView):
    template_name = 'reviews/feed.html'
    login_url = 'authentication:login'
    redirect_field_name = None

class PostView(ListView):
    pass


class FollowView(ListView):
    pass


