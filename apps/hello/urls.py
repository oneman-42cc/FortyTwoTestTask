from django.conf.urls import patterns, url
from hello.views import HomeView, RequestsListView, RequestsAsyncView,\
    MigrationsListView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^requests/$', RequestsListView.as_view(), name='requests'),
    url(r'^migrations/$', MigrationsListView.as_view(), name='migrations'),
    url(
        r'^requests/async/$',
        RequestsAsyncView.as_view(),
        name='requests-async',
    ),
)
