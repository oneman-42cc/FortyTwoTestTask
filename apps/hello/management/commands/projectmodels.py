from optparse import make_option
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            "--stream",
            default="stdout, stderr",
            dest="stream",
            help="Specifies the streams to which will print data.",
        ),
    )

    help = "Prints all project models and the count of objects in every model."

    def handle(self, *args, **options):

        # Parse param stream.
        streams = options.get("stream").split(", ")

        for type_ in ContentType.objects.all():

            model_ = type_.model_class()
            mname = str(model_).replace("<class '", "")\
                .replace("'>", "")
            # Count objects for each model and create output string.
            count = model_._default_manager.count()
            output = mname + " objects = " + str(count)

            if "stdout" in streams:
                self.stdout.write(output)

            if "stderr" in streams:
                self.stderr.write("error: " + output)
