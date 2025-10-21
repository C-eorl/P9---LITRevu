from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Value, CharField
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from .forms import ReviewForm, TicketForm, ReviewWithTicketForm
from .models import UserFollow, Ticket, Review, UserBlocked

User = get_user_model()


class UserTestCustom(UserPassesTestMixin):
    """
    UserTestCustom applique test_func() pour vérifier si l'utilisateur connecté est l'auteur du ticket &
    handle_no_permission() pour la redirection.
    """

    def test_func(self):
        element = self.get_object()
        return element.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission de modifier ce ticket.")
        return redirect("reviews:feed")


class FeedView(TemplateView):
    """ View pour le template feed.html """
    template_name = 'reviews/feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupère les tickets / critiques des utilisateurs auxquels je suis abonnées.

        # utilisateur que je suis
        followers_users = UserFollow.objects.filter(user=self.request.user) \
            .values_list('following_user', flat=True)
        # Récupère la liste des utilisateurs qui ont bloqué l'utilisateur connecté
        blocked_me = UserBlocked.objects.filter(blocked_user=self.request.user).values_list('user', flat=True)
        #inclus l'utilisateur connecté
        users_to_include = list(followers_users) + [self.request.user.id]

        # Tickets gestion
        tickets =(
            Ticket.objects
            .filter(user__in=users_to_include)
            .exclude(user__in=blocked_me)
            .annotate(content_type=Value("ticket", CharField()))
        )

        # Reviews gestion
        # Reviews publié par User et mes abonnements + les reviews sur les tickets User & abonnements
        reviews_from_users = Review.objects.filter(user__in=users_to_include)
        reviews_on_our_tickets = Review.objects.filter(ticket__user__in=users_to_include)

        reviews = (reviews_from_users | reviews_on_our_tickets).annotate(content_type=Value("review", CharField()))\
                                                    .exclude(user__in=blocked_me)\
                                                    .distinct()

        posts = sorted(
            chain(tickets, reviews),
            key=attrgetter('time_created'),
            reverse=True
        )

        # Récupère la liste des ID de ticket déjà critiqué
        reviewed_ticket_ids = Review.objects.values_list('ticket_id', flat=True)

        context['blocked_me'] = blocked_me
        context['reviewed_ticket_ids'] = reviewed_ticket_ids
        context['list_posts'] = posts
        return context


class PostView(TemplateView):
    """ View pour le template posts.html """
    template_name = 'reviews/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tickets = Ticket.objects.filter(user=self.request.user)
        reviews = Review.objects.filter(user=self.request.user)
        tickets = tickets.annotate(content_type=Value("ticket", CharField()))
        reviews = reviews.annotate(content_type=Value("review", CharField()))

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
    """ View pour créer un ticket """
    template_name = 'reviews/ticket_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Ticket
    form_class = TicketForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Ticket créé avec succès!')
        return response


class TicketUpdateView(UserTestCustom, UpdateView):
    """ View pour modifier un ticket """
    template_name = 'reviews/ticket_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Ticket
    form_class = TicketForm

    def form_valid(self, form):
        messages.success(self.request, 'Ticket modifié avec succès!')
        return super().form_valid(form)


class TicketDeleteView(UserTestCustom, DeleteView):
    """ View pour supprimer un ticket """
    model = Ticket
    template_name = 'reviews/ticket_delete.html'
    success_url = reverse_lazy('reviews:posts')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Ticket supprimé avec succès!')
        return super().delete(request, *args, **kwargs)


# ================================================================ #
#                         Critique                                 #
# ================================================================ #
class ReviewCreateView(CreateView):
    """Vue pour créer une critique (en réponse à un ticket ou libre)"""

    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Review

    def get_form_class(self):
        """Retourne le bon formulaire selon le contexte"""
        if self.kwargs.get('ticket_id'):
            # Réponse à un ticket existant
            return ReviewForm
        else:
            # Critique libre (avec création de ticket)
            return ReviewWithTicketForm

    def get_ticket(self):
        """ Récupère le ticket ou None"""
        tickets_id = self.kwargs.get('ticket_id')
        if tickets_id:
            return get_object_or_404(Ticket, pk=tickets_id)
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ticket = self.get_ticket()
        if ticket:
            context['ticket'] = ticket

        return context

    def form_valid(self, form):
        """Traite le formulaire selon le type de critique"""
        ticket = self.get_ticket()

        if ticket:
            # Réponse à un ticket existant
            form.instance.ticket = ticket
            form.instance.user = self.request.user
            messages.success(self.request, 'Critique créée avec succès!')
            return super().form_valid(form)
        else:
            # Critique libre avec création de ticket
            form.save(user=self.request.user)
            messages.success(self.request, 'Critique créée avec succès!')
            return redirect(self.success_url)

class ReviewUpdateView(UserTestCustom, UpdateView):
    """Vue pour modifier une critique existante"""

    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('reviews:posts')
    model = Review
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.object.ticket
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Critique modifiée avec succès!')
        return super().form_valid(form)


class ReviewDeleteView(UserTestCustom, DeleteView):
    """ View pour supprimer une critique """
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
    """ View pour le template follow.html """
    template_name = 'reviews/follow.html'

    def get_context_data(self, **kwargs):
        """ Récupère le context """
        context = super().get_context_data(**kwargs)
        context['followed_users'] = User.objects.filter(followers__user=self.request.user)
        context['followers'] = User.objects.filter(following__following_user=self.request.user)
        context['blocked_users'] = User.objects.filter(blocked_by__user=self.request.user)
        return context


def unfollow_user(request, user_id):
    """ View pour se désabonner d'un utilisateur """
    user_to_unfollow = User.objects.get(pk=user_id)
    UserFollow.objects.filter(user=request.user, following_user=user_to_unfollow).delete()
    messages.success(request, f"Vous n'êtes plus abonné(e) à {user_to_unfollow}")
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
    """
    View pour rechercher un utilisateur.
    Filtre par rapport à input utilisateur, exclus les utilisateurs deja abonné, soit meme et ceux bloqués.
    """

    query = request.GET.get("q", "")
    followed_ids = UserFollow.objects.filter(user=request.user) \
        .values_list('following_user_id', flat=True)
    blocked_user = UserBlocked.objects.filter(user=request.user).values_list('blocked_user_id', flat=True)

    users = User.objects.filter(username__icontains=query) \
        .exclude(pk__in=followed_ids) \
        .exclude(pk=request.user.pk) \
        .exclude(pk__in=blocked_user)[:10]

    data = [
        {
            "username": user.username,
            "image": user.profile_picture.url if user.profile_picture else "/static/pictures/default_pictures/default.png",
        }
        for user in users
    ]
    return JsonResponse(data, safe=False)


@require_POST
def blocked_user(request, user_id):
    """ Bloque un utilisateur """
    user_to_blocked = User.objects.get(pk=user_id)
    UserBlocked.objects.get_or_create(user=request.user, blocked_user=user_to_blocked)
    UserFollow.objects.filter(user=user_to_blocked, following_user=request.user).delete()

    messages.success(request, f"l'utilisateur {user_to_blocked.username} a été bloqué(e)")
    return redirect('reviews:follow')


@require_POST
def unblocked_user(request, user_id):
    """ Débloquer un utilisateur """
    unblocked_user = User.objects.get(pk=user_id)
    UserBlocked.objects.filter(user=request.user, blocked_user=unblocked_user).delete()
    messages.success(request, f"Vous avez débloqué {unblocked_user.username}")
    return redirect('reviews:follow')
