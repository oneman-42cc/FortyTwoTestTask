from django.test import TestCase
from django.utils import dateparse
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from hello.models import Profile


class HomePageTest(TestCase):

    """Test to check a view of home page - HomeView."""

    def setUp(self):
        self.response = self.client.get(reverse("home"))

    def test_accessibility_and_template(self):

        """This test checks whether available a home page and uses
            a right template."""

        self.assertEqual(self.response.status_code, 200)
        with self.assertTemplateUsed("hello/home.html"):
            render_to_string("hello/home.html")

    def test_page_title(self):

        """Test to check a page title."""

        self.assertContains(self.response, "42 Coffee Cups Test Assignment")

    def test_first_profile_item_in_context(self):

        """Test to check first Profile item in context."""

        profile_ctx = self.response.context["profile"]
        profile_db = Profile.objects.first()

        self.assertEqual(profile_ctx, profile_db)

    def test_present_data_in_html(self):

        """Test to check to present Profile data in HTML."""

        profile_ = Profile.objects.first()

        self.assertContains(self.response, profile_.email)
        self.assertContains(self.response, profile_.first_name)
        self.assertContains(self.response, profile_.last_name)
        self.assertContains(self.response, profile_.jabber)
        self.assertContains(self.response, profile_.skype)
        self.assertContains(self.response, profile_.birthday)

    def test_present_message_when_no_profile(self):

        """Test to check to present message on a page, when there is not
            profile."""

        # Remove all Profile object.
        Profile.objects.all().delete()
        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            "Sorry, I didn't fill out my cv. I'll do this in near future.",
        )

        self.assertNotContains(response, "oneman.test1@42cc.com")
        self.assertNotContains(response, "Oneman")
        self.assertNotContains(response, "Test1")
        self.assertNotContains(response, "jabber.bla1")
        self.assertNotContains(response, "skype.bla1")
        self.assertNotContains(
            response,
            dateparse.parse_date("2015-01-01"),
        )


class RequestsPageTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("requests"))

    def test_accessibility_and_template(self):

        """This test checks whether available a home page and uses
            a right template."""

        self.assertEqual(self.response.status_code, 200)
        with self.assertTemplateUsed("hello/requests.html"):
            render_to_string("hello/requests.html")