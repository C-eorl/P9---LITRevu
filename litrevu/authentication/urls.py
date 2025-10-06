from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import SignupView, redirection

app_name = 'authentication'

urlpatterns = [
    path('', redirection, name='redirect'),

    path('login/',
         LoginView.as_view(
            template_name='authentication/login.html',
            redirect_authenticated_user=True,
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='authentication:login'),name='logout'),
    path('signup/', SignupView.as_view(),name='signup'),
]
