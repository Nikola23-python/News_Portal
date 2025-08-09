from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import (Http404)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView, UpdateView, DeleteView, CreateView)

from .filters import PostFilter
from .forms import PostForm, SubscriptionForm
from .models import Post, Category


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['info'] = None
        return context
"""
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post', )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        if self.request.path == reverse('news_create'):
            post.post_type = 'NW'
        if self.request.path == reverse('article_create'):
            post.post_type = 'AR'
        post.save()
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.change_post'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post_type=self.post_type)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.post_type != self.post_type:
            raise Http404("Такой публикации не существует")
        return obj

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post_type=self.post_type)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.post_type != self.post_type:
            raise Http404("Такой публикации не существует")
        return obj



class PostSearchList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

# Новости
class NewsCreate(PostCreate):
    post_type = 'Новость'
    success_url = reverse_lazy('post_list')


class NewsUpdate(PostUpdate):
    post_type = 'Новость'
    success_url = reverse_lazy('post_list')


class NewsDelete(PostDelete):
    post_type = 'Новость'

# Статьи
class ArticleCreate(PostCreate):
    post_type = 'Статья'
    success_url = reverse_lazy('post_list')

class ArticleUpdate(PostUpdate):
    post_type = 'Статья'
    success_url = reverse_lazy('post_list')

class ArticleDelete(PostDelete):
    post_type = 'Статья'


@login_required
def subscribe(request, category_id=None):
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        category.subscribers.add(request.user)
        return redirect('category_posts', category_id=category_id)

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            request.user.subscriptions.set(form.cleaned_data['categories'])
            return redirect('subscription_success')
    else:
        form = SubscriptionForm(initial={
            'categories': request.user.subscriptions.all()
        })

    return render(request, 'sub/subscribe.html', {'form': form})

@login_required
def unsubscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)  # Удаляем пользователя из подписчиков
    return redirect('category_posts', category_id=category_id)

@login_required
def subscription_manage(request):
    categories = Category.objects.all()
    return render(request, 'sub/subscriptions.html', {
        'categories': categories
    })

def subscription_success(request):
    return render(request, 'sub/subscription_success.html')