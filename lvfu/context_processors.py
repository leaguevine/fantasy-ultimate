from django.conf import settings
from django.core.urlresolvers import reverse


_channel_path = None


def _get_channel_path():
    global _channel_path
    if not _channel_path:
        _channel_path = reverse('fb_channel_file')
    return _channel_path


def facebook(request):
    return {
        'fb_app_id': settings.FACEBOOK_APP_ID,
        'fb_permissions': settings.FACEBOOK_EXTENDED_PERMISSIONS,
        'fb_channel_file': request.build_absolute_uri(_get_channel_path())
    }
