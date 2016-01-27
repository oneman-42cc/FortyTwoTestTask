import time
import logging
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseForbidden
from django.core.management import call_command
from django.template.loader import render_to_string
from django.views import generic
from south.models import MigrationHistory
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

        """Returns context data for displaying the data of objects."""

        logger.debug(self.get_queryset())
        context = super(RequestsListView, self).get_context_data(**kwargs)
        logger.debug(context)

        return context


class MigrationsListView(generic.list.ListView):

    model = MigrationHistory
    template_name = "hello/migrations.html"

    def get_context_data(self, **kwargs):

        """Returns context data for displaying the data of objects."""

        context = super(MigrationsListView, self).get_context_data(**kwargs)

        call_command(
            "migrate",
            ignore_ghosts="--delete-ghost-migrations"
        )

        return context


class RequestsAsyncView(generic.View):

    def get(self, request, *args, **kwargs):

        """This method handle GET request.
            In this case return 403 error.
        """

        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):

        """This method handle POST request."""

        if not request.is_ajax():
            # If it is not AJAX request return 403 error.
            return HttpResponseForbidden()

        # Get number of new requests. It is tore only in HTML.
        counter = int(request.POST.get("numbernew", 0)) + 1

        # If there is not param test in POST request we handle
        # this request.
        if not request.POST.get("test"):

            seconds = 0
            seconds_max_waiting = 30
            # Count request items which was created from now.
            # In general it is 0.
            prev_number = Request.objects.filter(
                date__gt=request.time_,
            ).count()

            # Make timeout on seconds_max_waiting.
            # On which step of loop check or was created new request.
            while (seconds < seconds_max_waiting):
                # Count request items wich was created after 1 sec., 2 sec on
                # nex step, 3 sec on next etc.
                number_ = Request.objects.filter(
                    date__gt=request.time_,
                ).count()
                # If there is different beetwen numbers, update counter
                # and render data.
                if prev_number < number_:
                    counter += number_ - prev_number
                    return self.render_data(counter)

                seconds += 1
                time.sleep(1)
                prev_number = number_

        return self.render_data(counter)

    def render_data(self, counter):

        """Render data in JSON."""

        data_ = {
            "requests_new": counter if counter > 0 else "",
            "requests_list": render_to_string(
                "hello/request_list.html",
                {"object_list": Request.objects.all()[0:10]},
            ),
        }

        logger.debug(data_)

        return HttpResponse(
            simplejson.dumps(data_),
            content_type="application/json",
        )
