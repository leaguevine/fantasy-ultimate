from urlparse import urljoin

from django.conf import settings
from django.contrib.sites.models import Site


def site_base_url():
    return '%s://%s' % (settings.SITE_PROTOCOL,
                        Site.objects.get_current().domain)


def site_join_url(rel):
    return urljoin(site_base_url(), rel)
