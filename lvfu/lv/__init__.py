import json
import urllib
import urllib2
import urlparse

from django.conf import settings
from django.core.cache import cache

# Enforced by the Leaguevine API
MAX_PAGE_SIZE = 200


def make_list_qp(lst):
    return "[%s]" % ",".join([str(i) for i in lst])


def get_access_token(force_refresh=False, retries=2):
    if not force_refresh:
        token = cache.get('lv.access_token')
        if token:
            return token

    args = {
        'grant_type': 'client_credentials',
        'scope': 'universal',
        'client_id': settings.LEAGUEVINE_CLIENT_ID,
        'client_secret': settings.LEAGUEVINE_CLIENT_SECRET
    }

    tries = 0
    while True:
        try:
            f = urllib.urlopen("https://www.leaguevine.com/oauth2/token/",
                               data=urllib.urlencode(args))
            result = json.loads(f.read())
            token = result['access_token']
            cache.set('lv.access_token', token, 60 * 60 * 24 * 7)  # 1 week?
            return token
        except (urllib2.URLError, ValueError, KeyError):
            if tries == retries:
                raise
            tries += 1


class GetListRequest(object):
    def __init__(self, url, order_by=None, fields=None, page_size=MAX_PAGE_SIZE,
                 offset=None, **extra_data):
        if urlparse.urlparse(url).scheme:
            self.url = url
        else:
            self.url = "https://api.leaguevine.com/v1"
            if not url.startswith("/"):
                self.url += "/"
            self.url += url
        self.order_by = order_by
        self.fields = fields
        self.page_size = min(page_size, MAX_PAGE_SIZE) if page_size else None
        self.offset = offset
        self.extra_data = extra_data
        self.meta = None

    @property
    def has_more_pages(self):
        return not self.meta or self.meta['next']

    def get_next_page(self):
        if not self.has_more_pages:
            return None

        if self.meta:
            result = json.loads(urllib.urlopen(self.meta['next']).read())
        else:
            data = {}
            data.update(self.extra_data)
            if self.order_by is not None:
                data['order_by'] = make_list_qp(self.order_by)
            if self.fields is not None:
                data['fields'] = make_list_qp(self.fields)
            if self.page_size is not None:
                data['limit'] = self.page_size
            if self.offset is not None:
                data['offset'] = self.offset
            data['access_token'] = get_access_token()
            result = json.loads(urllib.urlopen(self.url + '?' + urllib.urlencode(data)).read())

        self.meta = result['meta']
        return result['objects']

    def get_all(self):
        all = []
        while self.has_more_pages:
            all.extend(self.get_next_page())
        return all

    #
    # Iterator semantics
    #
    def __iter__(self):
        return self

    def next(self):
        if not self.obj.has_more_pages:
            raise StopIteration
        return self.obj.get_next_page()
