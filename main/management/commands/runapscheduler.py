import logging
from django.contrib.auth.models import User
from main.models import Post
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


# наша задача по отправке еженедельной подборки новых объявлений всем пользователям
def weekly_newsletter():
    today = datetime.today()  # сегодня
    week_ago = today - timedelta(days=7)  # дата неделю назад
    email_list = User.objects.values_list('email', flat=True).distinct()
    for email in email_list:
        posts_list = Post.objects.filter(create_date__lt=week_ago)
        if posts_list:
            subject = f'Еженедельная подборка новых объявлений.'
            message = render_to_string(
                'mail_weekly_newsletter.html', {'posts': posts_list}
                )
            send_mail(subject, message, 'eretichok@yandex.ru', [email], fail_silently=False)


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            weekly_newsletter,
            # trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(
                day_of_week="mon", hour="08", minute="00"
            ),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="weekly_newsletter",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_newsletter'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
