import time

import requests

from sitechecker.models import Site


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.4f} seconds to execute")
        return result

    return wrapper


def check_site(site):
    return requests.head(site.url, allow_redirects=True)


def get_url_list():
    return Site.objects.all()
