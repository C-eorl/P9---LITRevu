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
from django.views.generic import TemplateView, CreateView, UpdateView, \
    DeleteView

from .forms import ReviewForm, TicketForm, ReviewWithTicketForm
from .models import UserFollow, Ticket, Review, UserBlocked

User = get_user_model()


class UserTestCustom(UserPassesTestMixin):
    """
    UserTestCustom inherits test_func() to check if the logged-in user is the ticket author &
    handle_no_permission() for redirection.
    """

    def test_func(self):
        element = self.get_object()
        return element.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request,
                       "Vous n'avez pas la permission de modifier ce ticket.")
        return redirect("reviews:feed")


class FeedView(TemplateView):
    """ View for template feed.html """
    template_name = 'reviews/feed.html'

    def get_context_data(self, **kwargs):
        """ Return context data for feed.html. """
        context = super().get_context_data(**kwargs)

        # following user
        following_users = UserFollow.objects.filter(user=self.request.user) \
            .values_list('following_user', flat=True)
        # Retrieves the list of users who have blocked the logged-in user.
        blocked_me = UserBlocked.objects.filter(
            blocked_user=self.request.user).values_list('user', flat=True)
        # including the logged-in user
        users_to_include = list(following_users) + [self.request.user.id]

        # Tickets management
        tickets = (
            Ticket.objects
            .filter(user__in=users_to_include)
            .exclude(user__in=blocked_me)
            .annotate(content_type=Value("ticket", CharField()))
        )

        # Reviews management
        # Reviews published by User and my subscriptions + reviews on User tickets & subscriptions
        reviews_from_users = Review.objects.filter(user__in=users_to_include)
        reviews_on_our_tickets = Review.objects.filter(
            ticket__user__in=users_to_include)

        reviews = (reviews_from_users | reviews_on_our_tickets).annotate(
            content_type=Value("review", CharField())) \
            .exclude(user__in=blocked_me) \
            .distinct()

        posts = sorted(
            chain(tickets, reviews),
            key=attrgetter('time_created'),
            reverse=True
        )

        # Retrieves the list of ticket IDs that have already been criticized.
        reviewed_ticket_ids = Review.objects.values_list('ticket_id', flat=True)

        context['blocked_me'] = blocked_me
        context['reviewed_ticket_ids'] = reviewed_ticket_ids
        context['list_posts'] = posts
        return context


class PostView(TemplateView):
    """ View for le template posts.html """
    template_name = 'reviews/posts.html'

    def get_context_data(self, **kwargs):
        """
        Return context data for posts.html
        Tickets & reviews from logged-in user.
        """
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
    """ View for create un ticket """
    template_name = 'reviews/ticket_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Ticket
    form_class = TicketForm

    def form_valid(self, form):
        """ Validate form data + message """
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Ticket créé avec succès!')
        return response


class TicketUpdateView(UserTestCustom, UpdateView):
    """ View for update ticket """
    template_name = 'reviews/ticket_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Ticket
    form_class = TicketForm

    def form_valid(self, form):
        """ Validate form data + message """
        messages.success(self.request, 'Ticket modifié avec succès!')
        return super().form_valid(form)


class TicketDeleteView(UserTestCustom, DeleteView):
    """ View for delete ticket """
    model = Ticket
    template_name = 'reviews/ticket_delete.html'
    success_url = reverse_lazy('reviews:posts')

    def delete(self, request, *args, **kwargs):
        """ Delete ticket + message """
        messages.success(request, 'Ticket supprimé avec succès!')
        return super().delete(request, *args, **kwargs)


# ================================================================ #
#                         Critique                                 #
# ================================================================ #
class ReviewCreateView(CreateView):
    """ View to create a review (in response to a ticket or freely) """

    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('reviews:feed')
    model = Review

    def get_form_class(self):
        """ Returns the correct form depending on the context """
        if self.kwargs.get('ticket_id'):
            # Reply to an existing ticket
            return ReviewForm
        else:
            # Free critique (with ticket creation)
            return ReviewWithTicketForm

    def get_ticket(self):
        """ Return the ticket or None"""
        tickets_id = self.kwargs.get('ticket_id')
        if tickets_id:
            return get_object_or_404(Ticket, pk=tickets_id)
        else:
            return None

    def get_context_data(self, **kwargs):
        """ Return context data for review.html """
        context = super().get_context_data(**kwargs)

        ticket = self.get_ticket()
        if ticket:
            context['ticket'] = ticket
        return context

    def form_valid(self, form):
        """ Process the form according to the type of review """
        ticket = self.get_ticket()

        if ticket:
            # Reply to an existing ticket + message
            form.instance.ticket = ticket
            form.instance.user = self.request.user
            messages.success(self.request, 'Critique créée avec succès!')
            return super().form_valid(form)
        else:
            # Free critique with ticket creation + message
            form.save(user=self.request.user)
            messages.success(self.request, 'Critique créée avec succès!')
            return redirect(self.success_url)


class ReviewUpdateView(UserTestCustom, UpdateView):
    """View to update review """

    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('reviews:posts')
    model = Review
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        """ Return context data (object ticket) for review.html """
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.object.ticket
        return context

    def form_valid(self, form):
        """ Validate form data + message"""
        messages.success(self.request, 'Critique modifiée avec succès!')
        return super().form_valid(form)


class ReviewDeleteView(UserTestCustom, DeleteView):
    """ View to delete review """
    model = Review
    template_name = 'reviews/review_delete.html'
    success_url = reverse_lazy('reviews:posts')

    def delete(self, request, *args, **kwargs):
        """ Delete ticket + message """
        messages.success(request, 'Critique supprimée avec succès!')
        return super().delete(request, *args, **kwargs)


# ================================================================ #
#                         Abonnements                              #
# ================================================================ #
class FollowView(TemplateView):
    """ View for template follow.html """
    template_name = 'reviews/follow.html'

    def get_context_data(self, **kwargs):
        """ Return context data for follow.html """
        context = super().get_context_data(**kwargs)
        context['followed_users'] = User.objects.filter(
            followers__user=self.request.user)
        context['followers'] = User.objects.filter(
            following__following_user=self.request.user)
        context['blocked_users'] = User.objects.filter(
            blocked_by__user=self.request.user)
        return context


def unfollow_user(request, user_id):
    """ function view to unfollow user + message """
    user_to_unfollow = User.objects.get(pk=user_id)
    UserFollow.objects.filter(user=request.user,
                              following_user=user_to_unfollow).delete()
    messages.success(request,
                     f"Vous n'êtes plus abonné(e) à {user_to_unfollow}")
    return redirect('reviews:follow')


@require_POST
def follow_user(request):
    """
    function view to follow user + message
    return Json
    """
    username = request.POST.get("username")
    user_to_follow = User.objects.get(username=username)
    UserFollow.objects.get_or_create(user=request.user,
                                     following_user=user_to_follow)
    return JsonResponse({"success": True})


@require_GET
def search_user(request):
    """
    View to search for a user.
    Filter based on user input, excluding users who are already subscribed,
    yourself, and those who are blocked.
    """

    query = request.GET.get("q", "")
    followed_ids = UserFollow.objects.filter(user=request.user) \
        .values_list('following_user_id', flat=True)
    blocked_user = UserBlocked.objects.filter(user=request.user).values_list(
        'blocked_user_id', flat=True)

    users = User.objects.filter(username__icontains=query) \
        .exclude(pk__in=followed_ids) \
        .exclude(pk=request.user.pk) \
        .exclude(pk__in=blocked_user)[:10]

    dir_default_img = "/static/pictures/default_pictures/default.png"
    data = [
        {
            "username": user.username,
            "image": user.profile_picture.url if user.profile_picture else dir_default_img,
        }
        for user in users
    ]
    return JsonResponse(data, safe=False)


@require_POST
def blocked_user(request, user_id):
    """ function view to block user + message """
    user_to_blocked = User.objects.get(pk=user_id)
    UserBlocked.objects.get_or_create(user=request.user,
                                      blocked_user=user_to_blocked)
    UserFollow.objects.filter(user=user_to_blocked,
                              following_user=request.user).delete()

    messages.success(request,
                     f"l'utilisateur {user_to_blocked.username} a été bloqué(e)")
    return redirect('reviews:follow')


@require_POST
def unblocked_user(request, user_id):
    """ function view to unblock user + message """
    unblocked_user = User.objects.get(pk=user_id)
    UserBlocked.objects.filter(user=request.user,
                               blocked_user=unblocked_user).delete()
    messages.success(request,
                     f"Vous avez débloqué {unblocked_user.username}")
    return redirect('reviews:follow')
