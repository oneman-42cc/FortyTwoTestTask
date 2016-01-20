from django.test import TestCase
from django.core.urlresolvers import reverse
from hello.models import Request


class RequestsLogMiddlewareTest(TestCase):

    def test_create_new_request_object(self):

        """Test for checking creation new Request object as page is
            viewed by user."""

        # Send requests to some pages.
        self.client.get(reverse("home"))

        self.assertEqual(Request.objects.count(), 1)
        request_ = Request.objects.first()
        self.assertEqual(request_.url, reverse("home"))
