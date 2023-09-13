from celery import shared_task
from .models import Post, Category
import datetime
from celery.schedules import crontab
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def weekly_sending():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    news = Post.objects.filter(time_in__gte=last_week)
    categories = set(Post.values_list('category__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        "daily_posts.html",
        {
            'link': 'http://127.0.0.1:8000',
            'posts': news
        }

    )

    msg = EmailMultiAlternatives(
        subject="НОВОСТИ ЗА НЕДЕЛЮ",
        body="",
        from_email='arczed@yandex.ru',
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_email_post(id):
    new = Post.objects.get(pk=id)
    categories = new.category.all()
    title = new.name
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for user in subscribers_users:
            subscribers_emails.append(user.email)

    html_content = render_to_string(
        'message.html',
        {
            'text': new.preview,
            'link': f"http://127.0.0.1:8000/news/{id}",
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='arczed@yandex.ru',
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
