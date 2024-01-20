from django.core.management.base import BaseCommand, CommandError
from sitechecker.models import Site


class Command(BaseCommand):
    help = "A Command to add a site url..."

    def add_arguments(self, parser):
        parser.add_argument("site", type=str)
        parser.add_argument("description", type=str)

    def handle(self, *args, **options):
        new_site = Site(site=options["site"], description=options["description"])

        try:
            new_site.save()
            self.stdout.write(self.style.SUCCESS("Site added %s - %s " % (options["site"], options["description"])))

        except Exception as e:
            self.stdout.write(self.style.ERROR("Something went wrong, %s."))
