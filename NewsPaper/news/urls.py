from django.urls import path
from .views import (PostsList, PostDetail, ArticleCreate, NewsCreate, NewsUpdate, NewsDelete,
ArticleUpdate, ArticleDelete, PostSearchList)

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearchList.as_view(), name='post_search'),

   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]