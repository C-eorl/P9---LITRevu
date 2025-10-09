from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import ListView, TemplateView

from .models import UserFollow
from authentication.models import User


class FeedView(TemplateView):
    template_name = 'reviews/feed.html'


class PostView(ListView):
    pass



class FollowView(TemplateView):
    template_name = 'reviews/follow.html'

    def get_context_data(self, **kwargs):
        # récupere context_object_name
        context = super().get_context_data(**kwargs)
        context['followed_users'] = User.objects.filter(followers__user=self.request.user)
        context['followers'] = User.objects.filter(following__following_user=self.request.user)
        return context


def unfollow_user(request, user_id):
    """
    Unfollow a user
    """
    user_to_unfollow = User.objects.get(pk=user_id)
    UserFollow.objects.filter(user=request.user, following_user=user_to_unfollow).delete()
    return redirect('reviews:follow')


@require_POST
def follow_user(request):
    """
    follow a user
    """
    username = request.POST.get("username")
    if not username:
        return JsonResponse({"success": False, "error": "Nom d'utilisateur manquant."})

    try:
        user_to_follow = User.objects.get(username=username)
        if user_to_follow == request.user:
            return JsonResponse({"success": False, "error": "Vous ne pouvez pas vous abonner à vous-même."})

        UserFollow.objects.get_or_create(user=request.user, following_user=user_to_follow)
        return JsonResponse({"success": True})
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "Utilisateur introuvable."})


@require_GET
def search_user(request):
    """
    Search user
    """
    query = request.GET.get("q", "")

    # IDs des utilisateurs que je suis déjà
    followed_ids = UserFollow.objects.filter(user=request.user).values_list('following_user_id', flat=True)

    # Recherche des utilisateurs correspondant à la query, en excluant moi-même et ceux que je suis déjà
    users = User.objects.filter(username__icontains=query) \
                        .exclude(pk__in=followed_ids) \
                        .exclude(pk=request.user.pk)[:10]

    data = [
        {
            "username": user.username,
            "image": user.profile_picture.url if user.profile_picture else "/static/pictures/default_pictures/default.png",
        }
        for user in users
    ]
    return JsonResponse(data, safe=False)