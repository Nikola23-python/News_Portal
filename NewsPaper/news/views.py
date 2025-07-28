from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from pyexpat.errors import messages

from .models import Post
from .filters import PostFilter
from .forms import PostForm

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

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

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



