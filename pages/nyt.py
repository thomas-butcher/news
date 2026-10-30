import requests
from django.conf import settings
from django.core.cache import cache

BASE_URL = "https://api.nytimes.com/svc"
CACHE_SECONDS = 60 * 15  # free keys are rate limited, so cache responses


class NytError(Exception):
    pass


def _get(path, cache_key):
    data = cache.get(cache_key)
    if data is not None:
        return data
    if not settings.NYT_API_KEY:
        raise NytError("NYT_API_KEY is not set.")
    try:
        r = requests.get(
            f"{BASE_URL}/{path}",
            params={"api-key": settings.NYT_API_KEY},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()["results"]
    except (requests.RequestException, KeyError, ValueError) as exc:
        raise NytError("Could not load stories from the New York Times.") from exc
    cache.set(cache_key, data, CACHE_SECONDS)
    return data


def top_stories(section="home"):
    return _get(f"topstories/v2/{section}.json", f"nyt_top_{section}")


def most_popular(period=1):
    return _get(f"mostpopular/v2/viewed/{period}.json", f"nyt_popular_{period}")
