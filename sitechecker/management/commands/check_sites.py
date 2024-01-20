"""
Perform an HTTP HEAD request and see if the site is up and return 200_OK message.
"""
from datetime import datetime

from django.core.management.base import BaseCommand
import requests
from django.utils import timezone

from sitechecker.models import Site, Check


def get_url_list():
    return Site.objects.all()


class Command(BaseCommand):
    help = "Check all sites."

    def handle(self, *args, **options):
        self.stdout.write("[*] Check all sites...")

        # perform http request
        for site in get_url_list():
            response = requests.head(site.url, allow_redirects=True)
            # TODO: Multi threads
            # TODO: tie a site to a user
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
            # Update database record to store the last response & timestamp.
