from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Response
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings
from .models import Profile


# после создания user, создается объект profile и прикрепляется к user
# (поля profile заполняются в редактировании профиля)
@receiver(post_save, sender=User)
def notify_post_author(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


# сигнал, отправляющий письмо автору поста, если кто-то написал сообщение на этот пост
@receiver(post_save, sender=Response)
def notify_new_response(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.user.username} написал сообщение к Вашему объявлению "{instance.post.headline}"'

        response = instance
        post = instance.post
        email = instance.post.author.email

        send_mail(
            subject=subject,
            message=render_to_string('mail-response_created_or_changed.html', {'response': response,
                                                                               'post': post}
                                     ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email]
        )
