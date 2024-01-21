from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from sitechecker.models import Site


class Command(BaseCommand):
    help = "A Command to add a site url..."

    def add_arguments(self, parser):
        parser.add_argument("url", type=str)
        parser.add_argument("description", type=str)
        parser.add_argument("username", type=str)

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options["username"])
        except ObjectDoesNotExist as e:
            raise CommandError("User not found, %s %s " % (options["username"], e))
        except MultipleObjectsReturned as e:
            raise CommandError("Multiple users match username, %s %s " % (options["username"], e))

        existing_match = Site.objects.filter(user=user, url=options["url"])
        if existing_match.exists():
            raise CommandError("Site already exist for user: %s & %s" % (user.username, options["url"]))

        new_site = Site(user=user, url=options["url"], description=options["description"])
        try:
            new_site.save()
            self.stdout.write(self.style.SUCCESS("Site added %s - %s " % (options["url"], options["description"])))
        except Exception:
            raise CommandError("Something went wrong, %s.")
