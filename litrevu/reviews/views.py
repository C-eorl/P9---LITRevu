from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms.models import modelform_factory
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from .models import UserFollow, Ticket, Review
from authentication.models import User


class UserTestCustom(UserPassesTestMixin):
    """
    UserTestCustom applique test_func() pour vérifier l'utilisateur connecté est l'auteur du ticket &
    handle_no_permission() pour la redirection.
    """
    def test_func(self):
        element = self.get_object()
        return element.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission de modifier ce ticket.")
        return redirect("reviews:feed")



class FeedView(TemplateView):
    template_name = 'reviews/feed.html'



class PostView(TemplateView):
    template_name = 'reviews/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tickets = Ticket.objects.filter(user=self.request.user)
        reviews = Review.objects.filter(user=self.request.user)

        for ticket in tickets:
            ticket.type = "ticket"
        for review in reviews:
            review.type = "review"

        posts = sorted(
            chain(tickets, reviews),
            key=attrgetter('time_created'),
            reverse=True
        )

        context['posts'] = posts
        return context

# ================================================================ #
#                         Ticket                                   #
# ================================================================ #
class TicketCreateView(CreateView):
    template_name = 'reviews/ticket_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Ticket
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Ticket créé avec succès!')
        return response


class TicketModifyView(UserTestCustom, UpdateView):
    """
    UserTestCustom applique test_func() pour vérifier l'utilisateur connecté est l'auteur du ticket &
    handle_no_permission() pour la redirection.
    """
    template_name = 'reviews/ticket_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Ticket
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        messages.success(self.request, 'Ticket modifié avec succès!')
        return super().form_valid(form)

class TicketDeleteView(UserTestCustom, DeleteView):
    model = Ticket
    template_name = 'reviews/ticket_delete.html'
    success_url = reverse_lazy('reviews:posts')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Ticket supprimé avec succès!')
        return super().delete(request, *args, **kwargs)

# ================================================================ #
#                         Critique                                 #
# ================================================================ #
class ReviewView(CreateView):
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Review
    fields = ['headline', 'rating', 'body']
    TicketForm = modelform_factory(Ticket, fields=['title', 'description', 'image'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_form"] = self.TicketForm(prefix="ticket")
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        ticket_form = self.TicketForm(self.request.POST, self.request.FILES, prefix="ticket")

        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = self.request.user
            ticket.save()
            form.instance.ticket = ticket
        else:
            return self.form_invalid(form)

        messages.success(self.request, "Ticket et Critique créés avec succès !")
        return super().form_valid(form)


class ReviewModifyView(UserTestCustom, UpdateView):
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Review
    fields = ['headline', 'rating', 'body']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.object.ticket
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Critique modifié avec succès!')
        return super().form_valid(form)

class ReviewDeleteView(UserTestCustom, DeleteView):
    model = Review
    template_name = 'reviews/review_delete.html'
    success_url = reverse_lazy('reviews:posts')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Critique supprimée avec succès!')
        return super().delete(request, *args, **kwargs)


# ================================================================ #
#                         Abonnements                              #
# ================================================================ #
class FollowView(TemplateView):
    template_name = 'reviews/follow.html'

    def get_context_data(self, **kwargs):
        # récupere context_object_name
        context = super().get_context_data(**kwargs)
        context['followed_users'] = User.objects.filter(followers__user=self.request.user)
        context['followers'] = User.objects.filter(following__following_user=self.request.user)
        return context


def unfollow_user(request, user_id):
    """ View pour se désabonner d'un utilisateur """
    user_to_unfollow = User.objects.get(pk=user_id)
    UserFollow.objects.filter(user=request.user, following_user=user_to_unfollow).delete()
    return redirect('reviews:follow')


@require_POST
def follow_user(request):
    """ View pour s'abonner d'un utilisateur """
    username = request.POST.get("username")
    if not username:
        return JsonResponse({"success": False, "error": "Nom d'utilisateur manquant."})

    user_to_follow = User.objects.get(username=username)
    UserFollow.objects.get_or_create(user=request.user, following_user=user_to_follow)
    return JsonResponse({"success": True})



@require_GET
def search_user(request):
    """ View pour rechercher un utilisateur """

    # filtre la recherche
    query = request.GET.get("q", "")
    followed_ids = UserFollow.objects.filter(user=request.user) \
                                     .values_list('following_user_id', flat=True)
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