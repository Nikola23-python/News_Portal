from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPaper1 import settings
from news.models import PostCategory


def send_notifications(preview, pk, post_title, subscribers):
    html_content = render_to_string('post_created_email.html',
        {
                'text': preview,
                'link': f'{settings.SITE_URL}/posts/{pk}'
            }
        )
    msg = EmailMultiAlternatives(
        subject=post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
        )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    (msg.send()

@receiver(post_save, sender=User))
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_mail(
            subject='Добро пожаловать в наш новостной портал!',
            message='',
            html_message=render_to_string('email/welcome.html', {
                'user': instance,
                'site_url': settings.SITE_URL
            }),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=True
        )

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.post_category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [subs.email for subs in subscribers]
        subscribers_emails = set(subscribers_emails)
        send_notifications(instance.preview(), instance.pk, instance.post_title, subscribers_emails)