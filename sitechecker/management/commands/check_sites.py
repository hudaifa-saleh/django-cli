"""
Perform an HTTP HEAD request and see if the site is up and return 200_OK message.
"""
from django.core.management.base import BaseCommand
import requests
from django.utils import timezone

from sitechecker.models import Site, Check


def get_url_list():
    return Site.objects.all()


def site_check(site):
    pass


class Command(BaseCommand):
    help = "Check all sites."

    def handle(self, *args, **options):
        self.stdout.write("[*] Check all sites...")

        with ThreadPoolExecutor(max_workers=24) as executor:
            future = executor.submit(pow, 323, 1235)
            print(future.result())

        # perform http request
        for site in get_url_list():
            response = requests.head(site.url, allow_redirects=True)
            self.stdout.write("Response For -->  %s - %s" % (response.status_code, site.url))
            site.last_response_code = str(response.status_code)
            site.last_response_checked = timezone.now()
            try:
                site.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR("Error updating check: %s - %s" % (e, site)))
            try:
                new_check_entry = Check(site=site, response_code=str(response.status_code))
                new_check_entry.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR("Error Adding check: %s - %s" % (e, new_check_entry)))
