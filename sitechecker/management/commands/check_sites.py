"""
Perform an HTTP HEAD request and see if the site is up and return 200_OK message.
"""
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from sitechecker.func import check_site
from sitechecker.models import Site, Check


class Command(BaseCommand):
    help = "Check all sites."

    def store_response(self, site, response):
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

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[*] Check all sites 😛"))

        with ThreadPoolExecutor(max_workers=settings.MAX_SITE_CHECKER_THREADS) as executor:
            future_to_responses = {executor.submit(check_site, site): site for site in Site.objects.all()}
            for future in concurrent.futures.as_completed(future_to_responses):
                site = future_to_responses[future]
                response = future.result()
                self.stdout.write("Response For -->  %s - %s" % (response.status_code, site.url))
                self.store_response(site, response)
