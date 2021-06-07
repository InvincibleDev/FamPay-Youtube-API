from django.core.management import BaseCommand, CommandError
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):

    help = "Set Periodic Task"

    def handle(self, *args, **options):
        try:
            every_50_seconds, _ = IntervalSchedule.objects.get_or_create(every=50, period=IntervalSchedule.SECONDS,)
            every_24_hours, _ = IntervalSchedule.objects.get_or_create(every=24, period=IntervalSchedule.HOURS,)

            PeriodicTask.objects.update_or_create(
                task="api.tasks.get_youtube_videos",
                name="Get Youtube Videos",
                defaults=dict(
                    interval=every_50_seconds,
                ),
            )

            PeriodicTask.objects.update_or_create(
                task="api.tasks.enable_api_keys",
                name="Enable API KEYS",
                defaults=dict(
                    interval=every_24_hours,
                ),
            )
        except Exception as e:
            raise CommandError(e)
