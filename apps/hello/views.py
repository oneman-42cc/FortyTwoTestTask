import logging
from django.views import generic
from hello.models import Profile, Request

logger = logging.getLogger("django")


class HomeView(generic.DetailView):

    """A view for home page. Renders user's profile."""

    model = Profile
    template_name = "hello/home.html"

    def get_object(self, queryset=None):

        """Returns the single object that this view will display.
            In this case it is first object of Profile.
        """

        return Profile.objects.first()

    def get_context_data(self, **kwargs):

        """Returns context data for displaying the data of objects."""

        context = super(HomeView, self).get_context_data(**kwargs)
        # Print to log data which passed to template.
        logger.debug(context)

        return context


class RequestsListView(generic.list.ListView):

    """A view for http requests page. Renders a table with last 10
        resuests and highliht as green new requests. As page is viewed
        by user all requests ar considered as read.
    """

    model = Request
    template_name = "hello/requests.html"
    queryset = Request.objects.all()[0:10]

    def get_context_data(self, **kwargs):

        logger.debug(self.get_queryset())
        context = super(RequestsListView, self).get_context_data(**kwargs)
        logger.debug(context)

        return context
