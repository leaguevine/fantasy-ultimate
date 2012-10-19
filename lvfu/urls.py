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

league_patterns = patterns(
    'lvfu.webapp.views',
    url(r'^$', 'league', name='league')
)

urlpatterns += patterns(
    'lvfu.webapp.views',
    (r'^$', "index"),
    (r'^welcome$', "welcome"),
    url(r'^newleague$', 'new_league', name='new_league'),
    url(r'^league/(?P<pk>[0-9]+)', include(league_patterns))
)
