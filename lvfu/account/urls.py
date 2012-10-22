from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^signout', 'django.contrib.auth.views.logout',
        {'next_page': "/"}, name='account_signout')
)
