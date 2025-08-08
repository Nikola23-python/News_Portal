from django.urls import path

from .views import (PostsList, PostDetail, ArticleCreate, NewsCreate, NewsUpdate, NewsDelete,
                    ArticleUpdate, ArticleDelete, PostSearchList, subscribe, unsubscribe, subscription_manage,
                    subscription_success)

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearchList.as_view(), name='post_search'),
   # публикация, редакция, удаление
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   # подписка, отписка, контроль подписок
   path('subscribe/', subscribe, name='subscribe'),
   path('unsubscribe/', unsubscribe, name='unsubscribe'),
   path('subscriptions/', subscription_manage, name='subscriptions'),
   path('subscription-success/', subscription_success, name='subscription_success'),
]