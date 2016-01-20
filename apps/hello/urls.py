from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'hello.views.home', name='home'),
)
