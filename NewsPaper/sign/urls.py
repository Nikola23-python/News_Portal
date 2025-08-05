from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import (BaseRegisterView, AddToAuthorsGroup)

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(http_method_names=['get', 'post'],template_name='sign/logout.html'),
         name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('add_to_authors/', AddToAuthorsGroup, name='add_to_authors'),
]
