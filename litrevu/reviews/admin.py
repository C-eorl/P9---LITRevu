from django.contrib import admin

from .models import Ticket, Review, UserFollow, UserBlocked


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """ Class Ticket for admin interface """
    list_display = ('title', 'user', 'time_created')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Class Review for admin interface """
    list_display = ('ticket', 'user', 'headline', 'time_created')


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    """ Class UserFollow for admin interface """
    list_display = ('user', 'following_user')


@admin.register(UserBlocked)
class UserBlockedAdmin(admin.ModelAdmin):
    """ Class UserBlocked for admin interface """
    list_display = ('user', 'blocked_user')
