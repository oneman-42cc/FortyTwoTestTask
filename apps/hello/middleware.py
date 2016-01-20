from apps.hello.models import Request


class RequestsLogMiddleware(object):

    def process_response(self, request, response):

        Request.objects.create(
            url=request.get_full_path(),
            user=request.user if request.user.is_authenticated() else None,
        )

        return response
