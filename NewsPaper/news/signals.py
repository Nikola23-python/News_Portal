from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
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
    msg.send()

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        post_categories = instance.categories.all()
        subscribers_emails = []

        for cat in post_categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [subs.email for subs in subscribers]
        subscribers_emails = set(subscribers_emails)
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)