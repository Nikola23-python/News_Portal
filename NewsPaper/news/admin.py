from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user__username',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
