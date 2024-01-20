from django.contrib import admin

from sitechecker.models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "site",
        "last_response_code",
    )
