from django.conf.urls.defaults import *

urlpatterns = patterns('flatpages_plus.views',
    # url(r'^(?P<url>.*)$',
    #     view='flatpage',
    #     name='flatpage'
    # ),
    (r'^(?P<url>.*)$', 'flatpage'),
)
