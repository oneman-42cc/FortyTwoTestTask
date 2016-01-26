from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from hello.models import Entry, Request


class SignalAnyModelPostSaveTest(TestCase):

    """Test to check a post_save signal."""

    def setUp(self):

        # Remove all etries.
        Entry.objects.all().delete()
        # Create a new object, e.g. of Request
        self.request_ = Request.objects.create(
            user=User.objects.first(),
            url=reverse("home"),
        )

    def test_creation_entry(self):

        """Test to check ot create the antry whan object
            is creation.
        """

        self.assertEqual(Entry.objects.count(), 1)

        entry_ = Entry.objects.first()
        self.assertEqual(entry_.content_object, self.request_)
        self.assertEqual(entry_.event, "creation")

    def test_editing_entry(self):

        """Test to check ot create the antry whan object
            is editing.
        """

        self.request_.save()
        self.assertEqual(Entry.objects.count(), 2)

        entry_ = Entry.objects.first()
        self.assertEqual(entry_.content_object, self.request_)
        self.assertEqual(entry_.event, "editing")

    def test_deletion_entry(self):

        """Test to check ot create the antry whan object
            is deletion.
        """

        self.request_.delete()
        self.assertEqual(Entry.objects.count(), 2)

        entry_ = Entry.objects.first()
        self.assertIsNone(entry_.content_object)
        self.assertEqual(entry_.event, "deletion")
