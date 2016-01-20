from django.test import TestCase
from django.utils import dateparse
from django.contrib.auth.models import User
from hello.models import Profile, Request


class ModelProfileTest(TestCase):

    """Test to check model Profile."""

    fixtures = ["profiles_test.json"]

    def test_or_save_profile_to_database(self):

        """Test to verify the model Profile."""

        self.assertEqual(Profile.objects.all().count(), 5)

        profile_ = Profile.objects.first()

        self.assertEqual(profile_.email, "oneman.test1@42cc.com")
        self.assertEqual(profile_.first_name, "Oneman")
        self.assertEqual(profile_.last_name, "Test1")
        self.assertEqual(profile_.jabber, "jabber.bla1")
        self.assertEqual(profile_.skype, "skype.bla1")
        self.assertEqual(
            profile_.birthday,
            dateparse.parse_date("2015-01-01"),
        )


class ModelRequestTest(TestCase):

    fixtures = ["requests_test.json"]

    def test_or_save_request_to_database(self):

        """Test to verify the model Request."""

        self.assertEqual(Request.objects.count(), 12)
        # Load Request object from database.
        request_ = Request.objects.get(id=1)

        self.assertEqual(request_.user, User.objects.get(id=1))
        self.assertEqual(request_.url, "http://127.0.0.1:8000/")
        self.assertEqual(
            request_.date,
            dateparse.parse_datetime("2016-01-04T17:31:39.112Z"),
        )
