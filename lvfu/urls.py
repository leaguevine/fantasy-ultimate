from django.conf.urls import patterns, include
from django.views.generic import RedirectView, TemplateView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^$', TemplateView.as_view(template_name='home.html')),
    (r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),
    (r'^admin/', include(admin.site.urls)),
)
