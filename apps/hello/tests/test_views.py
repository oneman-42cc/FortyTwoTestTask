from django.test import TestCase
from django.utils import dateparse, simplejson
from django.core.urlresolvers import reverse
from hello.models import Profile
from hello.forms import ProfileModelForm


class HomePageTest(TestCase):

    """Test to check a view of home page - HomeView."""

    def setUp(self):
        self.response = self.client.get(reverse("home"))

    def test_accessibility_and_template(self):

        """This test checks whether available a home page and uses
            a right template."""

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "hello/home.html")

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

    def test_present_photo(self):

        """Test to check or present photo on home page."""

        profile_ = Profile.objects.first()
        self.assertContains(self.response, profile_.photo.url)


class RequestsPageTest(TestCase):

    """Test to check a view of requests page - RequestsListView."""

    fixtures = ["requests_test.json"]

    def setUp(self):
        self.response = self.client.get(reverse("requests"))

    def test_accessibility_and_template(self):

        """This test checks whether available a home page and uses
            a right template."""

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "hello/requests.html")

    def test_check_number_items_in_context(self):

        """Test to check a number of items sends to templte.
            Must be 10."""

        self.assertEqual(
            self.response.context["object_list"].all().count(),
            10,
        )


class RequestsAsyncPageTest(TestCase):

    """Test to check a view of requests async page - RequestsAsyncView."""

    def test_accessibility(self):

        """This test checks whether available a requests async page."""

        # Send GET request.
        response = self.client.get(reverse("requests-async"))
        self.assertEqual(response.status_code, 403)
        # Send POST request.
        response = self.client.post(reverse("requests-async"))
        self.assertEqual(response.status_code, 403)
        # Send AJAX request.
        response = self.client.post(
            reverse("requests-async"),
            {"numbernew": 0, "test": True},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)

    def test_ajax_request(self):

        """Test to check AJAX request."""

        self.client.get(reverse("home"))

        # Send AJAX request. Mandatory parameter for test requests
        # is test=True. For detail see hello.views.RequestsAsyncView
        response = self.client.post(
            reverse("requests-async"),
            {"numbernew": 0, "test": True},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response["Content-Type"], "application/json")

        data_ = simplejson.loads(response._container[0])
        self.assertEqual(int(data_["requests_new"]), 1)
        self.assertIsNotNone(data_["requests_list"])


class LoginPageTest(TestCase):

    def test_accessibility_and_template(self):

        """This test checks whether available a login page and uses
            a right template."""

        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_user_logged(self):

        """Test to check login page."""

        self.client.get(reverse("login"))
        self.assertNotIn('_auth_user_id', self.client.session)

        response = self.client.post(
            reverse("login"),
            {"username": "admin", "password": "admin"},
        )
        self.assertIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse("home"), status_code=302)


class LogoutPageTest(TestCase):

    def test_accessibility(self):

        """This test checks whether available a logout page."""

        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"), status_code=302)
        self.assertNotIn('_auth_user_id', self.client.session)


class ProfileEditPageTest(TestCase):

    """Test to check a view of edit profile page - ProfileEditView."""

    def authorize_admin(self):

        """Helper method which authorize admin on the site."""

        # Authorize user admin.
        self.client.post(
            reverse("login"),
            {"username": "admin", "password": "admin"},
        )
        self.response = self.client.get(reverse("edit"))

    def test_accessibility_and_template(self):

        """This test checks whether available a edit page and uses
            a right template."""

        response = self.client.get(reverse("edit"))
        self.assertRedirects(
            response,
            reverse("login") + "?next=/edit/",
            status_code=302,
        )

        self.authorize_admin()

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "hello/edit.html")

    def test_check_context_data(self):

        """Test to check edit profile page."""

        self.authorize_admin()
        profile_ = Profile.objects.first()

        self.assertEqual(self.response.context["object"], profile_)
        self.assertEqual(
            self.response.context["form"].__class__,
            ProfileModelForm().__class__
        )

    def test_initial_data_of_edit_form(self):

        """Test to check initial data of edit profile form."""

        self.authorize_admin()

        profile_ = Profile.objects.first()
        data_ = self.response.context["form"].initial

        self.assertEqual(data_["email"], profile_.email)
        self.assertEqual(data_["first_name"], profile_.first_name)
        self.assertEqual(data_["last_name"], profile_.last_name)
        self.assertEqual(data_["birthday"], profile_.birthday)
        self.assertEqual(data_["jabber"], profile_.jabber)
        self.assertEqual(data_["skype"], profile_.skype)
        self.assertEqual(data_["bio"], profile_.bio)
        self.assertEqual(data_["contacts_other"], profile_.contacts_other)
        self.assertEqual(data_["photo"], profile_.photo)

    def test_required_fields_form(self):

        """Test to ckeck required fields. Required fields are: photo, email,
            first_name and last_name.
        """

        profile_ = Profile.objects.first()
        data_ = profile_.__dict__

        # Required fields are: photo, email, first_name and last_name.
        data_["photo"] = data_["email"] = data_["first_name"] = \
            data_["last_name"] = ""

        form = ProfileModelForm(data=data_)

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors["photo"][0],
            "This field is required.",
        )
        self.assertEqual(
            form.errors["email"][0],
            "This field is required.",
        )
        self.assertEqual(
            form.errors["first_name"][0],
            "This field is required.",
        )
        self.assertEqual(
            form.errors["last_name"][0],
            "This field is required.",
        )

    def test_or_update_profile_after_save_form(self):

        """Test to check or update profile data after form submition."""

        profile_ = Profile.objects.first()

        files_ = {"photo": profile_.photo}
        data_ = profile_.__dict__

        self.assertEqual(profile_.first_name, "One")
        self.assertEqual(profile_.last_name, "Man")

        # Change some data.
        data_["first_name"] = "One.Changed"
        data_["last_name"] = "Man.Changed"

        form = ProfileModelForm(data=data_, files=files_)
        if form.is_valid():
            form.save()

            self.assertEqual(profile_.first_name, "One.Changed")
            self.assertEqual(profile_.last_name, "Man.Changed")
