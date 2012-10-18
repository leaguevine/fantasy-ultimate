from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),
    (r'^admin/', include(admin.site.urls)),
    url(r'^channel.html$', 'fb_channel', name='fb_channel_file'),
    url(r'', include('social_auth.urls')),
)

urlpatterns += patterns('lvfu.views',
    (r'^$', "index"),
    (r'^welcome$', "welcome"),
)
