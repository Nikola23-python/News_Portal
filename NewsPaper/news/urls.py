from django.urls import path
from .views import (PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearchList)

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('update/<int:pk>', PostUpdate.as_view(), name='post_update'),
   path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearchList.as_view(), name='post_search'),
]