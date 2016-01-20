from django.conf.urls import patterns, url
from hello.views import HomeView, RequestsListView, RequestsAsyncView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^requests/$', RequestsListView.as_view(), name='requests'),
    url(
        r'^requests/async/$',
        RequestsAsyncView.as_view(),
        name='requests-async',
    ),
)
