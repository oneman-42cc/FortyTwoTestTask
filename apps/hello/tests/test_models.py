from django.test import TestCase
from django.utils import dateparse
from hello.models import Profile


class ModelProfileTest(TestCase):

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
