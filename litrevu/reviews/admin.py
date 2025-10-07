from django.contrib import admin

from .models import Ticket, Review, UserFollow


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'headline', 'time_created')

@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following_user')
