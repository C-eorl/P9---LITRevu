from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.views.generic import RedirectView

from .views import SignupView

app_name = 'authentication'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='authentication:login', permanent=False)),
    path('login/',
         LoginView.as_view(
             template_name='authentication/login.html',
         ),
         name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('signup/', SignupView.as_view(),name='signup'),
]
