from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import (Http404)
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, UpdateView, DeleteView, CreateView)

from .filters import PostFilter
from .forms import PostForm
from .models import Post


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

class PostCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
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

class PostDelete(DeleteView, LoginRequiredMixin):
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