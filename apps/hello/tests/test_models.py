from django.test import TestCase
from django.utils import dateparse
from django.contrib.auth.models import User
from hello.models import Profile, Request, Entry
from hello.tests.units import HelloAppTests


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
        self.assertEqual(profile_.photo, "profile/photo/oneman.png")
        self.assertEqual(profile_.jabber, "jabber.bla1")
        self.assertEqual(profile_.skype, "skype.bla1")
        self.assertEqual(
            profile_.birthday,
            dateparse.parse_date("2015-01-01"),
        )

    def test_size_of_photo(self):

        """Test to check a size of photo. On save image should be
            scale to size 200x200."""

        profile_ = Profile.objects.first()
        # Get temp photo. It has demenssions of 512x512px.
        photo_ = HelloAppTests.get_temporary_photo(pil=True)
        # Check size of original image.
        self.assertLessEqual(photo_.width, 512)
        self.assertLessEqual(photo_.height, 512)

        profile_.photo = photo_.fp
        profile_.save()

        # And check after save.
        self.assertLessEqual(profile_.photo.width, 200)
        self.assertLessEqual(profile_.photo.height, 200)


class ModelRequestTest(TestCase):

    """Test to check model Request."""

    fixtures = ["requests_test.json"]

    def test_or_save_request_to_database(self):

        """Test to verify the model Request."""

        self.assertEqual(Request.objects.count(), 12)
        # Load Request object from database.
        request_ = Request.objects.get(id=1)

        self.assertEqual(request_.user, User.objects.get(id=1))
        self.assertEqual(request_.url, "http://127.0.0.1:8000/")
        self.assertEqual(request_.priority, 0)
        self.assertEqual(
            request_.date,
            dateparse.parse_datetime("2016-01-04T17:31:39.112Z"),
        )


class ModelEntryTest(TestCase):

    """Test to check model Entry."""

    fixtures = ["entries_test.json"]

    def test_or_save_entry_to_database(self):

        """Test to verify the model Entry."""

        # First entry is information about profile.
        entry_ = Entry.objects.get(id=1)
        profile_ = Profile.objects.first()

        self.assertEqual(entry_.content_object, profile_)
        self.assertEqual(
            entry_.date,
            dateparse.parse_datetime("2016-01-26T00:53:26.420Z"),
        )
