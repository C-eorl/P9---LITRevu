from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from .models import UserFollow
from authentication.models import User


class FeedView(TemplateView):
    template_name = 'reviews/feed.html'


class PostView(ListView):
    pass



class FollowView(ListView):
    model = UserFollow
    template_name = 'reviews/follow.html'
    context_object_name = 'userfollows'

    def get_queryset(self):
        return UserFollow.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['followed_users'] = User.objects.filter(followers__user=self.request.user)
        context['followers'] = User.objects.filter(following__following_user=self.request.user)
        return context

def follow_user(request, user_id):
    user_to_follow = User.objects.get(pk=user_id)
    UserFollow.objects.get_or_create(user=request.user, following_user=user_to_follow)
    return redirect('reviews:follow')

def unfollow_user(request, user_id):
    user_to_unfollow = User.objects.get(pk=user_id)
    UserFollow.objects.filter(user=request.user, following_user=user_to_unfollow).delete()
    return redirect('reviews:follow')

def follow_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user_to_follow = User.objects.get(username=username)
            UserFollow.objects.get_or_create(user=request.user, following_user=user_to_follow)
        except User.DoesNotExist:
            pass  # tu peux gérer un message d'erreur ici
    return redirect('reviews:follow')