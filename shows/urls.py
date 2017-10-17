'''shows/urls.py - Contains the various non-administrative
url patterns that can be used on the site
and the views called by them.'''
from django.conf.urls import url

from . import views
from django.views.generic.base import RedirectView

app_name = 'shows'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^signup/$', views.signup, name='signup'),

    url(r'^home/$', views.index, name='home'),

    # urls for unsubscribing
    url(r'^unsubscribe', views.unsubscribe_results, name='unsubscribing'),
    url(r'^(?P<results>.+)/(?P<ids>.+)/(?P<images_1>.+)/(?P<images_2>.+)/unsubscribe_results/$', \
        views.unsubscribe, name='unsubscribe_results'),
    url(r'^(?P<results>.+)/(?P<ids>.+)/(?P<images_1>.+)/(?P<images_2>.+)/unsubscribe_results/unsub_to_shows/$', \
        views.unsub_to_shows, name='unsub_to_shows'),

    # urls for subscribing
    url(r'^home/search', views.searchShows, name='searching'),
    url(r'^(?P<results>.+)/(?P<ids>.+)/(?P<images_1>.+)/(?P<images_2>.+)/search_results/$', \
        views.search, name='search_results'),
    url(r'^(?P<results>.+)/(?P<ids>.+)/(?P<images_1>.+)/(?P<images_2>.+)/search_results/sub_to_shows/$', \
        views.sub_to_shows, name='sub_to_shows'),

    # favicon and menu icons
    url(r'^favicon\.png', RedirectView.as_view(url='/static/shows/images/favicon.png')),
    url(r'^menu\.png', RedirectView.as_view(url='/static/shows/images/menu.png')),
]