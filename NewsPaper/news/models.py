from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.urls import reverse




class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Рейтинг"
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def update_rating(self):
        # Суммарный рейтинг статей автора * 3
        post_rating = self.post_set.aggregate(
            post_rating=Sum('rating')
        ).get('post_rating', 0) * 3

        # Суммарный рейтинг комментариев автора
        comment_rating = self.user.comment_set.aggregate(
            comment_rating=Sum('rating')
        ).get('comment_rating', 0)

        # Суммарный рейтинг комментариев к статьям автора
        post_comment_rating = Comment.objects.filter(
            post__author=self
        ).aggregate(
            post_comment_rating=Sum('rating')
        ).get('post_comment_rating', 0)

        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return f"{self.user.username} (Рейтинг: {self.rating})"


class Category(models.Model):
    name = models.CharField(max_length=100,unique=True,verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [(ARTICLE, 'Статья'), (NEWS, 'Новость'),]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    post_type = models.CharField(max_length=2, choices=POST_TYPES, verbose_name="Тип публикации")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")
    categories = models.ManyToManyField(Category,through='PostCategory', verbose_name="Категории")
    title = models.CharField(max_length=200,verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    rating = models.IntegerField(default=0,validators=[MinValueValidator(0)],verbose_name="Рейтинг")
    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}'

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-created_at']

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.content[:124]}..." if len(self.content) > 124 else self.content

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.title} ({self.get_post_type_display()})"


class PostCategory(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Публикация"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Категория публикации"
        verbose_name_plural = "Категории публикаций"
        unique_together = [['post', 'category']]

    def __str__(self):
        return f"{self.post.title} | {self.category.name}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Публикация"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Рейтинг"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.post.title[:20]}..."


