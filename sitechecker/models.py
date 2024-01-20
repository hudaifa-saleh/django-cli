from django.contrib.auth.models import User
from django.db import models


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    last_response_code = models.CharField(max_length=10, null=True, blank=True)
    last_response_checked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(f"{self.user} / {self.site}")


class Check(models.Model):
    """
    The reason we're store the response code here in the checks we could omit the last response code and last time
    checked from the site, and you could just always do a lookup that says okay pull all the checks for that site,
    sort them by time and check the time on the last one and check the status code on the last one.
    But over time,
    if you've got millions and millions of these checks in the database, then every time you want to check the
    current status of your site you've got.
    """

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    response_code = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now_add=True)
