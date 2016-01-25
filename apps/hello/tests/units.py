import json
import os.path
import tempfile
from PIL import Image
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


class HelloAppTests(object):

    """It is a helper class for tsting of hello app."""

    @classmethod
    def authorize_admin(self, instance):

        """Helper method which authorize admin on the site."""

        # Authorize user admin.
        instance.client.post(
            reverse("login"),
            {"username": "admin", "password": "admin"},
        )
        return instance.client.get(reverse("edit"))

    @classmethod
    def get_temporary_photo(self, pil=False):

        """This method generates a temporary image, which load from
            fixtures. Use this method in general in tests.
            A temporary image has dimensions of 512x512px and extension
            of png.
        """

        # Set path to fixture with photo.
        fixture = os.path.join(
            os.path.dirname(__file__),
            "../fixtures/temporary_photo.json",
        )
        # Load and decode.
        photo = json.load(file(fixture)).get("photo", False)\
            .strip().decode("base64")

        # Create a temporary file and write to is data from fixtures.
        with tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False,
            dir=settings.MEDIA_ROOT,
        ) as png:
            png.write(photo)
            png.seek(0)
            image_ = SimpleUploadedFile(
                png.name,
                png.read(),
                content_type="image/png",
            )

            return Image.open(image_) if pil else image_

    @classmethod
    def set_temporary_photo(self, instance):

        """This method set a temporary image as a photo of profile. Use this
            method in general in tests.
        """

        image_ = self.get_temporary_photo()

        instance.photo = image_.name
        instance.save()
