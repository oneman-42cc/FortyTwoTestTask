from django.conf.urls import patterns, url
from hello.views import HomeView, RequestsListView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^requests/$', RequestsListView.as_view(), name='requests'),
)
