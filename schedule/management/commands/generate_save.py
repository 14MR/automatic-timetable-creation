from django.core.management.base import BaseCommand

from schedule.tasks import generate_table_and_save


class Command(BaseCommand):

    def handle(self, *args, **options):
        generate_table_and_save()

        self.stdout.write(self.style.SUCCESS('Successfully generated '))