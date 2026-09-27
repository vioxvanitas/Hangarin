
import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from tasks.models import Task, Note, SubTask, Priority, Category


class Command(BaseCommand):
    help = "Generate fake data for Hangarin"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of tasks to generate",
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options["count"]

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        if not priorities or not categories:
            self.stdout.write(
                self.style.ERROR(
                    "Please create Priority and Category records first."
                )
            )
            return

        statuses = ["Pending", "In Progress", "Completed"]

        for _ in range(count):
            deadline = timezone.make_aware(
                fake.date_time_this_month()
            )

            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=statuses),
                deadline=deadline,
                priority=random.choice(priorities),
                category=random.choice(categories),
            )

            # Generate 1 to 3 notes per task
            for _ in range(random.randint(1, 3)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

            # Generate 1 to 5 subtasks per task
            for _ in range(random.randint(1, 5)):
                SubTask.objects.create(
                    task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=statuses),
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated {count} tasks "
                "with notes and subtasks."
            )
        )