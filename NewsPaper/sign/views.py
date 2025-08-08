from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from news.models import Author  # Импортируем модель Author из вашего приложения


@login_required
def AddToAuthorsGroup(request):
    # Проверяем, не состоит ли пользователь уже в группе
    if not request.user.groups.filter(name='authors').exists():
        try:
            # Получаем группу авторов (или создаём, если не существует)
            authors_group, created = Group.objects.get_or_create(name='authors')

            # Добавляем пользователя в группу
            authors_group.user_set.add(request.user)

            # Создаём запись в Author, если её ещё нет
            if not hasattr(request.user, 'author'):
                Author.objects.create(user=request.user)

            # Можно добавить сообщение об успехе
            messages.success(request, 'Вы успешно добавлены в группу авторов!')
        except Exception as e:
            # Обработка возможных ошибок
            messages.error(request, f'Произошла ошибка: {str(e)}')

    return redirect('/')