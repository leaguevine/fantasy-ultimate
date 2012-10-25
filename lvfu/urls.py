from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),
    (r'^admin/', include(admin.site.urls)),
    url(r'^channel.html$', 'fb_channel', name='fb_channel_file'),
    url(r'', include('social_auth.urls')),

    (r'^account/', include('lvfu.account.urls')),
)

fragment_patterns = patterns(
    'lvfu.webapp.views',
    url(r'^roster$', 'fragment_roster', name='fragment_roster'),
    url(r'^team_rows$', 'fragment_team_rows', name='fragment_team_rows')
)

urlpatterns += patterns(
    'lvfu.webapp.views',
    url(r'^$', "index", name='index'),
    url(r'^my_team$', 'my_team', name='my_team'),
    url(r'^modify_team$', 'modify_team', name='modify_team'),
    url(r'^league$', 'league', name='league'),
    url(r'^rules$', 'rules', name='rules'),

    (r'^fragment/', include(fragment_patterns))
)
