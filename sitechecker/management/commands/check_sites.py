"""
Perform an HTTP HEAD request and see if the site is up and return 200_OK message.
"""
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
import requests

from sitechecker.models import Site


def get_url_list():
    return Site.objects.all()


class Command(BaseCommand):
    help = "Check all sites."

    def handle(self, *args, **options):
        self.stdout.write("[*] Check all sites...")

        # perform http request
        for site in get_url_list():
            response = requests.head(site.url)
            # TODO: Follow redirects
            # TODO: Multi threads
            # TODO: fix time
            self.stdout.write("Response: %s - %s" % (response.status_code, site.url))
            site.last_response_code = str(response.status_code)
            site.last_response_checked = datetime.now()
            site.save()
            # Update database record to store the last response & timestamp.
