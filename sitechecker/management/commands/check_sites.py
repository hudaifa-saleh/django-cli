"""
Perform an HTTP HEAD request and see if the site is up and return 200_OK message.
"""
from django.core.management.base import BaseCommand, CommandError
import requests


class Command(BaseCommand):
    help = "Check all sites."

    def handle(self, *args, **options):
        self.stdout.write("[*] Check all sites...")

        # perform http request
        for site_url in list_of_url:
            site_url = "https://www.djangoproject.com"
            response = requests.head(site_url)
            self.stdout.write("Response: %s" % response.status_code)
            # Update database record to store the last response & timestamp.
