from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, Response
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings
# from main.tasks import new_post_mail
from .models import Profile


# после создания user, создается объект profile и прикрепляется к user
# (поля profile заполняются в редактировании профиля)
@receiver(post_save, sender=User)
def notify_post_author(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


# рассылка подписчикам: новая публикация в категории, на которую пользователи подписаны
# @receiver(post_save, sender=Response)
# def notify_post_author(sender, instance, created, **kwargs):
#     if created:
#         subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
#     else:
#         subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'
#     post = Post.objects.get(author=instance.post.author)
#     send_mail(
#         subject=subject,
#         message=instance.message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list='[email]'
#     )
    # if action == "post_add":
    #     post_categories = instance.category.filter(pk__in=pk_set).distinct()
    # email_list = SubscribeCategory.objects.filter(category__in=post_categories).values_list('user__email',
    #                                                                                         flat=True).distinct()
    # post_categories_name = ', '.join(instance.category.values_list('category_name', flat=True))
    # if email_list:
    #     for email in email_list:
    #         subject = f"Вышла новая публикация в категории {post_categories_name}."
    #         message = render_to_string('post_created.html', {'post': instance})
    #         send_mail(
    #                         subject=subject,
    #                         message=message,
    #                         from_email=settings.DEFAULT_FROM_EMAIL,
    #                         recipient_list=[email]
    #                     )


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


# # сигнал, отправляющий письмо автору сообщения, если автор поста принял/отменил принятие сообщения
# @receiver(post_save, sender=Response)
# def notify_response_is_accepted_changed(sender, instance, created, update_fields, **kwargs):
#     if not created and 'is_accepted' in update_fields:
#         if instance.is_accept:
#             subject = f'Автор объявления {instance.post.headline} принял Ваше предложение.'
#         else:
#             subject = f'Автор объявления {instance.post.headline} отменил принятие Вашего предложения/'
#         response = instance
#         post = instance.post
#         email = instance.user.email
#         message = render_to_string('mail-response_is_accepted_changed.html', {'response': response,
#                                                                               'post': post}
#                                    )
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[email]
#         )