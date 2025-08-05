import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from .models import BaseRegisterForm

sys.path.append("..")
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()
from ..news.models import Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def AddToAuthorsGroup(request):  # добавление пользователя в группу с правами автора
    if not request.user.groups.filter(name='authors').exists():
        authors_group = Group.objects.get(name='authors')
        user = request.user
        authors_group.user_set.add(user)

        # добавление пользователя как автора в модель Authors

        Author.objects.create(user=request.user)
    return redirect('/')