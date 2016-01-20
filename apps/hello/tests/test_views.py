from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string


class HomePageTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("home"))

    def test_accessibility_and_template(self):

        """This test checks whether available a home page and uses
            a right template."""

        self.assertEqual(self.response.status_code, 200)
        with self.assertTemplateUsed('hello/home.html'):
            render_to_string('hello/home.html')

    def test_page_title(self):

        """Test to check a page title."""

        self.assertContains(self.response, "42 Coffee Cups Test Assignment")
