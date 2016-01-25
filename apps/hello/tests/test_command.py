from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.contrib.contenttypes.models import ContentType


class projectmodelsCommandTest(TestCase):

    def get_models_list(self):

        """Helper method which generate array of models with
            number of object of each.
        """

        models = []

        for type_ in ContentType.objects.all():

            model_ = type_.model_class()
            # Count objects for each model and create output string.
            count = model_._default_manager.count()
            models.append(str(model_) + " objects = " + str(count))

        return models

    def setUp(self):
        # Get list of models.
        self.models = self.get_models_list()

    def test_command_run_with_default_params(self):

        """Test run a command with deafult params."""

        streamout = StringIO()
        streamerr = StringIO()
        call_command(
            "projectmodels",
            stdout=streamout,
            stderr=streamerr,
        )

        for m in self.models:
            self.assertIn(m, streamout.getvalue())
            self.assertIn("error: " + m, streamerr.getvalue())

    def test_run_with_stream_stdout(self):

        """Test run a command with param stream equal stdout."""

        streamout = StringIO()
        streamerr = StringIO()
        call_command(
            "projectmodels",
            stream="stdout",
            stdout=streamout,
            stderr=streamerr,
        )

        for m in self.models:
            self.assertIn(m, streamout.getvalue())
            self.assertNotIn("error: " + m, streamerr.getvalue())

    def test_run_with_stream_stderr(self):

        """Test run a command with param stream equal stderr."""

        streamout = StringIO()
        streamerr = StringIO()
        call_command(
            "projectmodels",
            stream="stderr",
            stdout=streamout,
            stderr=streamerr,
        )

        for m in self.models:
            self.assertNotIn(m, streamout.getvalue())
            self.assertIn("error: " + m, streamerr.getvalue())
