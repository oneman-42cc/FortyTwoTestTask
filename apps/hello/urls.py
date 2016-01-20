from django.conf.urls import patterns, url
from hello.views import HomeView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^requests/$', 'hello.views.requests_list_page', name='requests'),
)
