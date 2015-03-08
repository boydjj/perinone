from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'perinone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^orders/', include('orders.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
