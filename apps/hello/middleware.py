import datetime
from apps.hello.models import Request


class RequestsLogMiddleware(object):

    """This middleware stores all http requests in the DB,
        by creting new object of Request.
    """

    def process_request(self, request):

        # On each request create new object of Request.
        Request.objects.create(
            url=request.get_full_path(),
            user=request.user if request.user.is_authenticated() else None,
        )
        # Add to request a time whan it was send.
        # This time uses in hello.view.RequestsAsyncView.
        request.time_ = datetime.datetime.now()
