from django.core.management.base import BaseCommand, CommandError

from schedule.tasks import generate_table


class Command(BaseCommand):

    def handle(self, *args, **options):
        generate_table()

        self.stdout.write(self.style.SUCCESS('Successfully generated '))