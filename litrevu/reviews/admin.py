from django.contrib import admin

from .models import Ticket, Review, UserFollow


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    pass
