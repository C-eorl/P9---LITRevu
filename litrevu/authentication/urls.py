from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import SignupView, redirection, CustomLoginView

app_name = 'authentication'

urlpatterns = [
    path('', redirection, name='redirect'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='authentication:login'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]
