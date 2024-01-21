from sitechecker.models import Site


def get_url_list():
    return Site.objects.all()


def site_check(site):
    pass
